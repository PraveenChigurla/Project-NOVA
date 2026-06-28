"""
Rollback Manager.
Executes the defined RollbackPolicy for any previously successful steps to restore system state.
"""

import logging
from typing import List

from nova.intelligence.planning.models import PlanStep
from nova.execution.models import StepResult

logger = logging.getLogger(__name__)

class RollbackManager:
    """Manages system state restoration on critical failures."""
    
    @staticmethod
    async def execute_rollback(
        failed_step_id: str,
        execution_history: List[StepResult],
        plan_steps: List[PlanStep],
        execution_engine # The ExecutionEngine instance
    ) -> None:
        """
        Traverse backwards through successful steps and execute their rollback policies.
        """
        logger.critical(f"CRITICAL FAILURE at Step '{failed_step_id}'. Initiating Rollback sequence...")
        
        # Create lookup for step policies
        step_map = {s.step_id: s for s in plan_steps}
        
        # Traverse history in reverse (most recent first)
        for result in reversed(execution_history):
            if not result.success:
                continue # Only rollback successful steps
                
            step_def = step_map.get(result.step_id)
            if not step_def or not step_def.rollback_policy:
                logger.debug(f"Step '{result.step_id}' has no rollback policy. Skipping.")
                continue
                
            policy = step_def.rollback_policy
            logger.warning(f"Executing rollback for step '{result.step_id}' -> Action: {policy.action} on {policy.capability_id}")
            
            try:
                # Ask the engine to execute the rollback action bypassing normal flow
                # We do this directly to avoid polluting the execution plan graph
                await execution_engine._execute_capability_action(
                    capability_id=policy.capability_id,
                    action=policy.action,
                    parameters=policy.parameters,
                    context_vars={} # Rollbacks usually don't need the forward context
                )
                result.rolled_back = True
                logger.info(f"Rollback for step '{result.step_id}' succeeded.")
            except Exception as e:
                logger.error(f"Rollback for step '{result.step_id}' FAILED! System may be in an inconsistent state. Error: {e}")
