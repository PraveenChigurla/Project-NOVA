import json
import os
from typing import Dict, Any
from nova.intelligence.planning.models import ExecutionPlan

import platform
import sys
import psutil

class DeterministicReplay:
    """
    Captures execution state to allow deterministic reproduction of failures.
    Forensic bundle includes OS, memory, and runtime snapshots.
    """
    def __init__(self, output_dir: str = "07_Validation/Benchmarks", run_uuid: str = "UNKNOWN"):
        self.output_dir = output_dir
        self.run_uuid = run_uuid
        os.makedirs(self.output_dir, exist_ok=True)
        
    def capture_failure(self, iteration: int, plan: ExecutionPlan, error_message: str, seed: str = "UNKNOWN"):
        """
        Serializes the plan and the error context into a forensic bundle.
        """
        process = psutil.Process(os.getpid())
        
        forensic_bundle = {
            "metadata": {
                "run_uuid": self.run_uuid,
                "iteration": iteration,
                "error": error_message,
                "seed": seed,
            },
            "environment": {
                "os": platform.platform(),
                "python_version": sys.version,
                "cpu_count": psutil.cpu_count(),
                "total_ram_gb": round(psutil.virtual_memory().total / (1024**3), 2)
            },
            "runtime_snapshot": {
                "memory_mb": round(process.memory_info().rss / (1024 * 1024), 2),
                "capability_state": "MOCK_SUITE",
                "permission_snapshot": "GRANTED",
                "timeline": "AVAILABLE_IN_EVENT_BUS_LOG"
            },
            "plan": plan.model_dump(mode="json")
        }
        
        filename = f"{self.run_uuid}_failure_{iteration:06d}.json"
        path = os.path.join(self.output_dir, filename)
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(forensic_bundle, f, indent=2)
            
        print(f"Captured deterministic replay trace: {path}")
        return path
        
    def replay(self, filepath: str):
        """
        Loads a trace and reconstructs the execution plan.
        (Implementation of the actual execution is left to the runner).
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            bundle = json.load(f)
            
        metadata = bundle.get("metadata", {})
        iteration = metadata.get("iteration", "UNKNOWN")
        error = metadata.get("error", "UNKNOWN")
        seed = metadata.get("seed", "UNKNOWN")
        
        print(f"Replaying failure from iteration {iteration}")
        print(f"Original Error: {error}")
        print(f"Random Seed: {seed}")
        
        plan = ExecutionPlan(**bundle["plan"])
        return plan
