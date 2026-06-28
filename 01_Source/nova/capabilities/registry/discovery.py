"""
Capability Discovery and Loading.
Provides mechanisms to find and instantiate capabilities.
"""

from typing import List
import logging

from nova.capabilities.base import Capability, CapabilityMetadata
from nova.capabilities.hello_capability import HelloCapability

logger = logging.getLogger(__name__)

class CapabilityDiscovery:
    """
    Discovers capabilities from the environment or built-in modules.
    For Phase 1, it manually loads the HelloCapability reference implementation.
    """
    def __init__(self, permission_manager=None, provider_registry=None):
        self.permission_manager = permission_manager
        self.provider_registry = provider_registry
        
    def discover_builtins(self) -> List[Capability]:
        """Discover built-in capabilities statically defined in the codebase."""
        capabilities = []
        
        # Instantiate HelloCapability
        meta = CapabilityMetadata(
            id="com.nova.hello",
            name="Hello Capability",
            version="1.0.0",
            description="The first reference capability",
            tags=["demo", "system"],
            supported_intents=["say_hello", "read_file"]
        )
        
        hello_cap = HelloCapability(meta, permission_manager=self.permission_manager)
        capabilities.append(hello_cap)
        
        # Instantiate ProcessCapability
        if self.provider_registry:
            from nova.capabilities.desktop.process import ProcessCapability
            process_meta = CapabilityMetadata(
                id="com.nova.desktop.process",
                name="Process Capability",
                version="1.0.0",
                description="Manages OS processes",
                tags=["desktop", "system"],
                supported_intents=["launch_process", "terminate_process", "is_process_running", "list_processes"]
            )
            process_cap = ProcessCapability(process_meta, permission_manager=self.permission_manager, provider_registry=self.provider_registry)
            capabilities.append(process_cap)
        
        logger.info(f"Discovered {len(capabilities)} built-in capabilities.")
        return capabilities

class CapabilityLoader:
    """
    Loads discovered capabilities into a registry.
    """
    def __init__(self, registry, discovery: CapabilityDiscovery):
        self._registry = registry
        self._discovery = discovery
        
    async def load_all(self) -> None:
        """Discover and register all available capabilities."""
        builtins = self._discovery.discover_builtins()
        
        for cap in builtins:
            try:
                await self._registry.register(cap)
            except Exception as e:
                logger.error(f"Failed to load capability {cap.metadata.id}: {e}")
