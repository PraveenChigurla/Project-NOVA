"""
Execution Scheduler.
Resolves dependency layers and schedules steps for execution.
"""

import logging
from typing import List

from nova.intelligence.planning.models import PlanStep, ExecutionStrategy
from nova.intelligence.planning.graph import TaskGraph

logger = logging.getLogger(__name__)

class ExecutionScheduler:
    """Computes the execution path for a plan."""
    
    @staticmethod
    def compute_layers(steps: List[PlanStep], strategy: ExecutionStrategy) -> List[List[PlanStep]]:
        """
        Returns a list of execution layers.
        If SEQUENTIAL, each layer has exactly 1 step (in dependency order).
        If PARALLEL, layers contain multiple independent steps that can be run via asyncio.gather.
        """
        if not steps:
            return []
            
        graph = TaskGraph(steps)
        # This inherently validates the graph for cycles and missing dependencies
        parallel_layers = graph.get_execution_layers()
        
        if strategy == ExecutionStrategy.SEQUENTIAL:
            logger.info("Scheduler forcing SEQUENTIAL execution.")
            # Flatten the parallel layers into strictly sequential layers
            sequential_layers = []
            for layer in parallel_layers:
                for step in layer:
                    sequential_layers.append([step])
            return sequential_layers
            
        logger.info(f"Scheduler computed {len(parallel_layers)} PARALLEL execution layers.")
        return parallel_layers
