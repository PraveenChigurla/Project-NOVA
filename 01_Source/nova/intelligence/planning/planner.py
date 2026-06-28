"""
Planner Base Class and Implementations.
The intelligence orchestrators that convert intents into Execution Plans.
"""

from abc import ABC, abstractmethod
from typing import Optional
import time
import logging

from nova.intelligence.planning.models import (
    PlannerContext,
    PlannerResult,
    ExecutionPlan,
    PlanStep,
    ExecutionStrategy
)
from nova.intelligence.planning.graph import TaskGraph
from nova.intelligence.intents.models import IntentResult

logger = logging.getLogger(__name__)

class Planner(ABC):
    """
    Abstract base class for all Planners.
    """
    
    @abstractmethod
    async def generate_plan(self, intent: IntentResult, context: Optional[PlannerContext] = None) -> ExecutionPlan:
        """
        Parses the intent and constructs an ExecutionPlan.
        Must be implemented by subclasses.
        """
        pass
        
    async def plan(self, intent: IntentResult, context: Optional[PlannerContext] = None) -> PlannerResult:
        """
        Template method that wraps plan generation with validation and profiling.
        """
        start_time = time.perf_counter()
        
        try:
            logger.info(f"Planner beginning generation for intent: '{intent.intent_name}'")
            execution_plan = await self.generate_plan(intent, context)
            
            # Validate the graph mathematically
            graph = TaskGraph(execution_plan.steps)
            graph.validate()
            
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            
            logger.info(f"Planner successfully generated plan '{execution_plan.plan_id}' with {len(execution_plan.steps)} steps.")
            return PlannerResult(
                success=True,
                plan=execution_plan,
                elapsed_ms=elapsed_ms
            )
            
        except Exception as e:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            logger.error(f"Planner failed to generate plan: {e}")
            return PlannerResult(
                success=False,
                error_message=str(e),
                elapsed_ms=elapsed_ms
            )

class RuleBasedPlanner(Planner):
    """
    A simple planner for Phase 1 that uses hardcoded rules to generate static plans.
    """
    async def generate_plan(self, intent: IntentResult, context: Optional[PlannerContext] = None) -> ExecutionPlan:
        
        if intent.intent_name == "desktop.process.launch":
            app_name = intent.entities.get("application", "notepad.exe")
            # If the user didn't specify extension, append .exe for windows
            if not app_name.endswith(".exe"):
                app_name += ".exe"
                
            step = PlanStep(
                capability_id="com.nova.desktop.process",
                action="launch_process",
                parameters={"executable": app_name},
                dependencies=[]
            )
            
            return ExecutionPlan(
                intent=intent.original_input,
                strategy=ExecutionStrategy.SEQUENTIAL,
                steps=[step]
            )
            
        elif intent.intent_name == "complex_workflow":
            # Generate a DAG to test parallel execution
            step1 = PlanStep(step_id="step1", capability_id="com.nova.vision", action="scan", dependencies=[])
            step2 = PlanStep(step_id="step2", capability_id="com.nova.vision", action="analyze", dependencies=["step1"])
            step3 = PlanStep(step_id="step3", capability_id="com.nova.desktop", action="click", dependencies=["step1"])
            step4 = PlanStep(step_id="step4", capability_id="com.nova.browser", action="navigate", dependencies=["step2", "step3"])
            
            return ExecutionPlan(
                intent=intent.original_input,
                strategy=ExecutionStrategy.PARALLEL,
                steps=[step1, step2, step3, step4]
            )
            
        raise ValueError(f"RuleBasedPlanner does not understand intent: '{intent.intent_name}'")
