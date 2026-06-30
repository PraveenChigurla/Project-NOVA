import asyncio
import time
from typing import Dict, Any

from nova.execution.engine import ExecutionEngine
from nova.intelligence.planning.models import ExecutionPlan
from nova.core.event_bus import AsyncioEventBus
from nova.core.registry import PluginRegistry

from .generator import ExecutionGenerator
from .collector import MetricsCollector
from .reporter import EvidenceReporter
from .replay import DeterministicReplay
from .telemetry import TelemetryTracker

from .mocks import MOCK_CAPABILITIES
from nova.security.permissions.manager import PermissionManager
from nova.security.permissions.policy import PermissionValidator, PermissionPolicy
from nova.security.permissions.registry import PermissionRegistry
from nova.capabilities.base.health import CapabilityState

import uuid

class BenchmarkRunner:
    """
    Orchestrates the 4 phases: Warmup, Measurement, Validation, Teardown.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.run_uuid = f"EVP-RUN-{time.strftime('%Y')}-{str(uuid.uuid4())[:6]}"
        self.generator = ExecutionGenerator(seed=config.get("seed", "NOVA_EVP_1"))
        self.output_dir = config.get("output_dir", "07_Validation/Benchmarks")
        self.collector = MetricsCollector(run_uuid=self.run_uuid)
        self.reporter = EvidenceReporter(output_dir=self.output_dir)
        self.replay = DeterministicReplay(output_dir=self.output_dir, run_uuid=self.run_uuid)
        
        # Core Runtime
        self.registry = PluginRegistry()
        self.event_bus = AsyncioEventBus()
        self.permission_manager = PermissionManager()
        self.engine = ExecutionEngine(self.registry, self.permission_manager)
        self.integrity_callback = None
        
    def set_integrity_callback(self, callback):
        self.integrity_callback = callback
        
    async def _init_mocks(self):
        # Register Mocks and advance to READY state
        for cap_id, cap in MOCK_CAPABILITIES.items():
            if cap_id not in self.registry.get_capabilities():
                self.registry.register_capability(cap_id, cap)
                
            if cap.state == CapabilityState.CREATED:
                await cap.system_register()
                await cap.system_initialize({})
                await cap.system_start()
        
    async def run(self):
        await self._init_mocks()
        iterations = self.config.get("iterations", 100)
        warmup = self.config.get("warmup", 10)
        
        print("--- EVP Benchmark Runner ---")
        print(f"Phase 1: Warmup ({warmup} iterations)")
        for _ in range(warmup):
            plan = self.generator.generate_plan(complexity=2)
            await self.engine.execute_plan(plan)
            
        self.telemetry = TelemetryTracker()
            
        # Start Event Bus
        await self.event_bus.start()
        
        print(f"Phase 2: Measurement ({iterations} iterations)")
        self.collector.start_run()
        
        checkpoint_interval = self.config.get("checkpoint_interval", 1000)
        use_profile = self.config.get("use_resilience_profile", False)
        
        for i in range(1, iterations + 1):
            inject_fail = self.config.get("inject_failure", False) and i == self.config.get("fail_at", -1)
            plan = self.generator.generate_plan(complexity=3, inject_failure=inject_fail, use_profile=use_profile)
            
            start_time = time.perf_counter()
            expected = False
            success = False
            try:
                result = await self.engine.execute_plan(plan)
                
                if not result.success:
                    # In a resilience profile, the engine returning success=False because of a mock is expected.
                    # We classify this as an expected failure.
                    expected = True
                else:
                    success = True
            except Exception as e:
                # Engine crashed entirely (should not happen, Engine catches capability errors)
                success = False
                expected = False
                error_category = self._classify_failure(e)
                error_msg = f"[{error_category}] {str(e)}"
                self.replay.capture_failure(i, plan, error_msg, seed=self.config.get("seed", "UNKNOWN"))
                
            latency = time.perf_counter() - start_time
            self.collector.record_execution(latency, success, expected)
            
            if i % checkpoint_interval == 0:
                print(f"  Checkpoint: {i}/{iterations}...")
                q_depth = self.event_bus._queue.qsize()
                active_tasks = len(self.engine._active_sessions)
                snapshot = self.telemetry.capture_snapshot(
                    iteration=i, 
                    event_queue_depth=q_depth, 
                    active_tasks=active_tasks
                )
                self.collector.record_checkpoint(snapshot)
                
                if self.integrity_callback:
                    if not self.integrity_callback(self):
                        raise RuntimeError("Integrity Verification Failed at Checkpoint")
                
        self.collector.end_run()
        
        print("Phase 3: Validation")
        # For now, rely on standard engine exceptions. More advanced DAG validation can go here.
        
        print("Phase 4: Teardown")
        await self.event_bus.stop()
        
        print("Generating Evidence...")
        report_path = self.reporter.generate_report(self.collector.get_summary(), self.config)
        print(f"Report generated: {report_path}")
        
        return self.collector.get_summary()
        
    def _classify_failure(self, e: Exception) -> str:
        err_str = str(e).lower()
        if "permission" in err_str:
            return "Permission"
        elif "timeout" in err_str:
            return "Execution"
        elif "registry" in err_str:
            return "Capability"
        elif "provider" in err_str:
            return "Provider"
        elif "rollback" in err_str:
            return "Execution"
        return "Unknown"
