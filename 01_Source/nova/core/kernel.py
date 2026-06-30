import asyncio
import logging
import signal
import sys
from typing import Optional

from .config import NovaConfig
from .di import ServiceLocator
from .event_bus import IEventBus, AsyncioEventBus
from nova.capabilities.registry import CapabilityRegistry, LifecycleCoordinator, CapabilityDiscovery, CapabilityLoader
from nova.security.permissions import PermissionManager
from nova.providers.registry import ProviderRegistry, ProviderLifecycleCoordinator, ProviderDiscovery, ProviderLoader
from nova.execution.engine import ExecutionEngine
from nova.execution.models import ExecutionResult, SessionState
from nova.intelligence.intents.models import Intent, IntentAlias, IntentResult
from nova.intelligence.intents.registry import IntentRegistry
from nova.intelligence.intents.parser import RuleIntentParser
from nova.intelligence.planning.planner import RuleBasedPlanner
from nova.skills.loader import SkillRegistry, SkillLoader
from nova.security.vault.core import SecretVault

logger = logging.getLogger(__name__)

class NovaKernel:
    """
    Project NOVA Core Orchestrator.
    Manages the lifecycle of the entire platform.
    """
    def __init__(self, config: NovaConfig):
        self.config = config
        self.locator = ServiceLocator()
        
        self.provider_registry = ProviderRegistry()
        self.provider_lifecycle = ProviderLifecycleCoordinator(self.provider_registry)
        
        self.registry = CapabilityRegistry()
        self.lifecycle = LifecycleCoordinator(self.registry)
        
        self.permission_manager = PermissionManager()
        self.execution_engine = ExecutionEngine(self.registry, self.permission_manager)
        
        self.secret_vault = SecretVault()
        
        self.skill_registry = SkillRegistry()
        self.skill_loader = SkillLoader(self.skill_registry)
        
        # Intelligence Pipeline
        self.intent_registry = IntentRegistry()
        self.intent_parser = RuleIntentParser(self.intent_registry)
        self.planner = RuleBasedPlanner()
        
        self._shutdown_event = asyncio.Event()
        self._task_group: Optional[asyncio.TaskGroup] = None
        self._is_running = False

    def _setup_signal_handlers(self) -> None:
        """Register graceful shutdown handlers for SIGINT/SIGTERM."""
        if sys.platform != 'win32':
            loop = asyncio.get_running_loop()
            for sig in (signal.SIGINT, signal.SIGTERM):
                loop.add_signal_handler(sig, self._initiate_shutdown, sig)
        else:
            # Basic handler for Windows
            signal.signal(signal.SIGINT, lambda s, f: self._initiate_shutdown(s))
            signal.signal(signal.SIGTERM, lambda s, f: self._initiate_shutdown(s))

    def _initiate_shutdown(self, sig: int) -> None:
        logger.warning(f"Received termination signal ({sig}). Initiating graceful shutdown...")
        self._shutdown_event.set()

    async def _health_monitor(self) -> None:
        """Background watchdog task for basic health monitoring."""
        event_bus = self.locator.resolve(IEventBus)
        try:
            while not self._shutdown_event.is_set():
                await asyncio.sleep(10)
                if self._is_running:
                    logger.debug("Kernel Watchdog: System health OK")
                    await event_bus.publish("System.Health.Ping", {"status": "OK"})
        except asyncio.CancelledError:
            logger.debug("Kernel Watchdog cancelled")
            
    async def _handle_abort(self, payload: dict) -> None:
        logger.critical(f"System Abort Requested: {payload.get('reason', 'Unknown')}")
        self._shutdown_event.set()

    async def boot(self) -> None:
        """Initialize the kernel, bind dependencies, and start infrastructure."""
        logger.info("Starting NOVA Kernel Boot Sequence...")
        
        # Setup Dependency Injection
        logger.debug("Initializing Dependency Injection Container...")
        event_bus = AsyncioEventBus(max_queue_size=self.config.event_bus_max_queue_size)
        
        self.locator.register_instance(IEventBus, event_bus)
        self.locator.register_instance(ProviderRegistry, self.provider_registry)
        self.locator.register_instance(CapabilityRegistry, self.registry)
        
        # Start Event Bus
        await event_bus.start()
        event_bus.subscribe("System.Abort.Requested", self._handle_abort)
        
        # 1. Discover, Load, and Boot Providers
        prov_discovery = ProviderDiscovery()
        prov_loader = ProviderLoader(self.provider_registry, prov_discovery)
        await prov_loader.load_all()
        await self.provider_lifecycle.boot_all({})
        
        # 2. Discover, Load, and Boot Capabilities
        discovery = CapabilityDiscovery(
            permission_manager=self.permission_manager,
            provider_registry=self.provider_registry
        )
        loader = CapabilityLoader(self.registry, discovery)
        await loader.load_all()
        
        # Boot Capabilities (Topological Order)
        global_config = {"com.nova.hello": {"setting": True}}
        await self.lifecycle.boot_all(global_config)
        
        # Setup Intelligence Base
        self._register_default_intents()
        
        # Setup signal handlers
        self._setup_signal_handlers()
        
        logger.info("NOVA Kernel Boot Sequence Complete")
        await event_bus.publish("System.Boot.Complete", {"version": "0.8.0"})

    def _register_default_intents(self):
        """Registers the standard capability intents."""
        launch_intent = Intent(
            name="desktop.process.launch",
            description="Launches a desktop application.",
            required_entities=["application"],
            aliases=[
                IntentAlias(
                    pattern=r"(?:open|launch|start|run)\s+([a-zA-Z0-9_\-\.]+)",
                    entities_map={1: "application"}
                ),
                IntentAlias(
                    pattern=r"(?:can you please)?\s*(?:open|launch|start|run)\s+([a-zA-Z0-9_\-\.]+)\s*(?:for me)?",
                    entities_map={1: "application"}
                )
            ]
        )
        self.intent_registry.register(launch_intent)

    async def execute_command(self, raw_input: str) -> Optional[ExecutionResult]:
        """
        The End-to-End Orchestrator Pipeline.
        1. Parses intent from natural language.
        2. Generates an execution plan.
        3. Executes the plan securely.
        """
        logger.info(f"\n[{'='*50}]\nNOVA Processing Input: '{raw_input}'\n[{'='*50}]")
        
        # 1. Intent Parsing
        intent_res = await self.intent_parser.parse(raw_input)
        if not intent_res.is_valid or intent_res.intent_name == "unknown":
            logger.warning(f"Aborting execution. Input could not be resolved to a valid intent.")
            return None
            
        # 2. Planning
        planner_res = await self.planner.plan(intent_res)
        if not planner_res.success or not planner_res.plan:
            logger.error(f"Aborting execution. Planner failed: {planner_res.error_message}")
            return None
            
        # 3. Execution
        execution_res = await self.execution_engine.execute_plan(planner_res.plan)
        return execution_res

    async def run(self) -> None:
        """Main execution loop using TaskGroup for safe concurrency."""
        if self._is_running:
            return
            
        self._is_running = True
        logger.info("Entering Kernel execution loop...")
        
        try:
            async with asyncio.TaskGroup() as tg:
                self._task_group = tg
                tg.create_task(self._health_monitor())
                
                # Wait until shutdown is requested
                shutdown_task = tg.create_task(self._shutdown_event.wait())
                await shutdown_task
                
        except Exception as e:
            logger.critical(f"Kernel Panic: {e}", exc_info=True)
        finally:
            await self.shutdown()

    async def shutdown(self) -> None:
        """Gracefully teardown all components."""
        if not self._is_running:
            return
            
        logger.info("Starting Graceful Teardown...")
        self._is_running = False
        
        try:
            await self.lifecycle.shutdown_all()
        except Exception as e:
            logger.error(f"Error shutting down capabilities: {e}")
            
        try:
            await self.provider_lifecycle.shutdown_all()
        except Exception as e:
            logger.error(f"Error shutting down providers: {e}")
            
        try:
            event_bus: AsyncioEventBus = self.locator.resolve(IEventBus) # type: ignore
            await event_bus.stop()
        except Exception as e:
            logger.error(f"Error stopping Event Bus: {e}")
            
        self.locator.clear()
        logger.info("NOVA Kernel safely terminated.")
