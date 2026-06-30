import uuid
import random
from typing import List, Optional
from nova.intelligence.planning.models import ExecutionPlan, PlanStep

class ExecutionGenerator:
    """
    Synthesizes rapid, deterministic ExecutionPlans for stress testing the runtime.
    """
    
    def __init__(self, seed: Optional[str] = None):
        self.seed = seed or "NOVA_EVP_1"
        self._counter = 0
        self.rng = random.Random(self.seed)
        
        # Capability distribution matrix
        self.resilience_profile = [
            ("mock.succeed", 0.70),
            ("mock.retry", 0.10),
            ("mock.fail", 0.08),
            ("mock.rollback", 0.05),
            ("mock.timeout", 0.03),
            ("mock.permission_denied", 0.02),
            ("mock.cancel", 0.02)
        ]

    def _select_capability(self) -> str:
        r = self.rng.random()
        cumulative = 0.0
        for cap, prob in self.resilience_profile:
            cumulative += prob
            if r <= cumulative:
                return cap
        return "mock.succeed"

    def generate_plan(self, complexity: int = 3, inject_failure: bool = False, use_profile: bool = False) -> ExecutionPlan:
        """
        Generates a deterministic plan containing `complexity` number of mock tasks.
        If `use_profile` is True, it will select capabilities based on the resilience distribution matrix.
        Otherwise, it defaults to `mock.succeed` (unless `inject_failure` is forced).
        """
        self._counter += 1
        plan_id = f"plan_{self.seed}_{self._counter}"
        
        steps = []
        for i in range(complexity):
            if use_profile:
                target = self._select_capability()
            else:
                target = "mock.succeed"
                
            if inject_failure and i == complexity - 1:
                target = "mock.fail"
                
            step = PlanStep(
                step_id=f"{plan_id}_step_{i}",
                capability_id=target,
                action="execute",
                parameters={"iteration": self._counter, "step": i, "task_id": f"{plan_id}_step_{i}"},
                dependencies=[f"{plan_id}_step_{i-1}"] if i > 0 else []
            )
            steps.append(step)
            
        return ExecutionPlan(
            plan_id=plan_id,
            intent="Benchmark execution",
            steps=steps
        )
