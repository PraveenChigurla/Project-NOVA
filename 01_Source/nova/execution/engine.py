"""
Execution Engine.
The primary runtime component that bridges Execution Plans to Capabilities.
"""

import asyncio
import time
import logging
from typing import Dict, Any

from nova.intelligence.planning.models import ExecutionPlan, PlanStep
from nova.capabilities.registry import CapabilityRegistry
from nova.security.permissions import PermissionManager, PermissionRequest, PermissionScope
from nova.capabilities.base import CapabilityRequest

from nova.execution.models import (
    ExecutionSession, 
    SessionState, 
    StepResult, 
    ExecutionResult
)
from nova.execution.managers import (
    ExecutionScheduler,
    RetryManager,
    RollbackManager,
    CancellationManager,
    ExecutionCancelledError
)

logger = logging.getLogger(__name__)

class ExecutionEngine:
    """Orchestrates the execution of plans."""
    
    def __init__(self, capability_registry: CapabilityRegistry, permission_manager: PermissionManager):
        self._capability_registry = capability_registry
        self._permission_manager = permission_manager
        
        # We track active sessions so they can be paused/cancelled remotely
        self._active_sessions: Dict[str, CancellationManager] = {}

    async def execute_plan(self, plan: ExecutionPlan) -> ExecutionResult:
        """
        Main entry point for execution.
        """
        start_time = time.perf_counter()
        session = ExecutionSession(plan_id=plan.plan_id, state=SessionState.RUNNING)
        cancellation = CancellationManager()
        self._active_sessions[session.session_id] = cancellation
        
        logger.info(f"Execution Engine starting session {session.session_id} for plan {plan.plan_id}")
        
        try:
            # 1. Schedule layers
            layers = ExecutionScheduler.compute_layers(plan.steps, plan.strategy)
            
            # 2. Execute layers sequentially (steps within a layer run in parallel if strategy allows)
            for layer_idx, layer in enumerate(layers):
                await cancellation.check_state()
                logger.debug(f"Executing Layer {layer_idx} with {len(layer)} step(s)...")
                
                # Create tasks for all steps in the layer
                tasks = [
                    self._execute_step_with_retry(step, session, cancellation)
                    for step in layer
                ]
                
                # Wait for the layer to finish
                layer_results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Check for critical failures in the layer
                for step, result in zip(layer, layer_results):
                    if isinstance(result, BaseException):
                        # A step threw an unhandled exception (e.g., cancelled or total failure)
                        raise result
                        
                    session.step_results[step.step_id] = result
                    if not result.success:
                        logger.error(f"Step {step.step_id} failed critically. Halting execution.")
                        raise Exception(f"Step {step.step_id} failed: {result.error}")
                        
            session.state = SessionState.COMPLETED
            
        except ExecutionCancelledError as e:
            logger.warning(f"Session {session.session_id} cancelled.")
            session.state = SessionState.CANCELLED
            
        except Exception as e:
            logger.error(f"Session {session.session_id} failed: {e}")
            session.state = SessionState.FAILED
            
            # Initiate Rollback Sequence
            logger.info("Executing RollbackManager...")
            await RollbackManager.execute_rollback(
                failed_step_id="unknown", # We could track this more precisely
                execution_history=list(session.step_results.values()),
                plan_steps=plan.steps,
                execution_engine=self
            )
            session.state = SessionState.ROLLED_BACK
            
        finally:
            if session.session_id in self._active_sessions:
                del self._active_sessions[session.session_id]
                
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            success = session.state == SessionState.COMPLETED
            
            return ExecutionResult(
                plan_id=session.plan_id,
                session_id=session.session_id,
                success=success,
                state=session.state,
                step_results=list(session.step_results.values()),
                error_message=None if success else f"Execution ended with state {session.state.value}",
                total_elapsed_ms=elapsed_ms
            )

    async def _execute_step_with_retry(self, step: PlanStep, session: ExecutionSession, cancellation: CancellationManager) -> StepResult:
        """Wraps step execution in the retry manager."""
        
        async def _run_step():
            return await self._execute_capability_action(
                capability_id=step.capability_id,
                action=step.action,
                parameters=step.parameters,
                context_vars=session.context.variables
            )
            
        step_start = time.perf_counter()
        retries_used = 0
        success = False
        data = {}
        error_msg = None
        
        try:
            # We track retries by wrapping the execution func.
            # But getting exact retry count requires extending RetryManager slightly, 
            # for now we'll just let RetryManager handle it and if it returns, it succeeded.
            # If it raises, it failed.
            data = await RetryManager.execute_with_retry(
                step_id=step.step_id,
                policy=step.retry_policy,
                cancellation=cancellation,
                func=lambda: asyncio.wait_for(_run_step(), timeout=step.timeout_ms / 1000.0)
            )
            success = True
        except asyncio.TimeoutError:
            error_msg = f"Step {step.step_id} timed out after {step.timeout_ms}ms"
            logger.error(error_msg)
        except asyncio.CancelledError:
            error_msg = f"Step {step.step_id} was cancelled"
            logger.warning(error_msg)
        except Exception as e:
            error_msg = str(e)
            
        step_elapsed = (time.perf_counter() - step_start) * 1000
        
        return StepResult(
            step_id=step.step_id,
            capability_id=step.capability_id,
            action=step.action,
            success=success,
            data=data,
            error=error_msg,
            retries_used=retries_used,
            elapsed_ms=step_elapsed
        )

    async def _execute_capability_action(self, capability_id: str, action: str, parameters: Dict[str, Any], context_vars: Dict[str, Any]) -> Dict[str, Any]:
        """
        The lowest level of the engine.
        1. Resolves Capability.
        2. Checks Permission.
        3. Executes.
        """
        # 1. Resolve Capability
        cap = await self._capability_registry.get(capability_id)
        if not cap:
            raise ValueError(f"Capability '{capability_id}' not found in registry.")
            
        # 2. Check Permissions (Automatic mapping based on action for now, or require explicit scopes in the plan)
        # For Phase 1, we map certain actions to scopes. Ideally, capabilities declare scopes they need for actions.
        # We will assume a 1:1 mapping for demonstration, or we bypass for internal safe actions.
        required_scope = None
        if action == "read_file":
            required_scope = PermissionScope.OS_FILES_READ
        elif action == "launch_process":
            required_scope = PermissionScope.OS_PROCESS_START
        elif action == "terminate_process":
            required_scope = PermissionScope.OS_PROCESS_KILL
        elif action in ["capture_full_desktop", "capture_active_monitor", "capture_monitor", "capture_region"]:
            required_scope = PermissionScope.OS_WINDOW_CAPTURE
            
        if required_scope:
            perm_req = PermissionRequest(capability_id=capability_id, scope=required_scope)
            perm_result = await self._permission_manager.evaluate(perm_req)
            if not perm_result.is_allowed:
                raise PermissionError(f"Permission Framework blocked execution: {perm_result.message}")
        
        # 3. Execute
        cap_req = CapabilityRequest(
            capability_id=capability_id,
            action=action,
            payload=parameters
        )
        
        cap_res = await cap.run(cap_req)
        if not cap_res.success:
            raise RuntimeError(f"Capability failed: {cap_res.error}")
            
        return cap_res.data
