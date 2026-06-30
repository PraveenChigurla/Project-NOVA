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
    async def generate_plan(self, cognitive_package, context: Optional[PlannerContext] = None) -> ExecutionPlan:
        """
        Parses the enriched cognitive package and constructs an ExecutionPlan.
        Must be implemented by subclasses.
        """
        pass
        
    async def plan(self, cognitive_package, context: Optional[PlannerContext] = None) -> PlannerResult:
        """
        Template method that wraps plan generation with validation and profiling.
        """
        start_time = time.perf_counter()
        
        try:
            logger.info(f"Planner beginning generation for Goal: '{cognitive_package.goal.id}'")
            execution_plan = await self.generate_plan(cognitive_package, context)
            
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
    A simple planner that generates static plans, now enriched by the Cognitive Layer.
    """
    async def generate_plan(self, cognitive_package, context: Optional[PlannerContext] = None) -> ExecutionPlan:
        goal = cognitive_package.goal
        world = cognitive_package.world
        constraints = cognitive_package.constraints
        
        if constraints.ask_user_confirmation:
            logger.info("Constraints mandate user confirmation before planning. Emitting ASK_USER step.")
            step = PlanStep(
                capability_id="com.nova.core",
                action="ask_user",
                parameters={"prompt": "Constraints dictate confirmation required. Proceed?"},
                dependencies=[]
            )
            return ExecutionPlan(
                intent=goal.raw_intent,
                strategy=ExecutionStrategy.SEQUENTIAL,
                steps=[step]
            )

        if goal.id == "prepare_workspace":
            steps = []
            
            # Utilize Memory!
            if cognitive_package.memory:
                mem = cognitive_package.memory
                
                # Semantic
                for fact in mem.relevant_facts:
                    if fact.key == "preferred_ide":
                        logger.info(f"Memory: User prefers IDE '{fact.value}' (confidence: {fact.confidence})")
                        
                # Episodic
                if mem.recent_episodes:
                    logger.info(f"Memory: Found {len(mem.recent_episodes)} recent episodes related to workspace prep.")
                    for ep in mem.recent_episodes:
                        logger.info(f"  - Episode: {ep.summary}")
            
            # Use WorldGraph to avoid redundant work!
            world = cognitive_package.world
            
            # Check if IDE is running
            ide_apps = [e for e in world.get_entities_by_type("Application") if "code" in e.attributes.get("name", "").lower() or "vscode" in e.attributes.get("name", "").lower()]
            if not ide_apps:
                steps.append(PlanStep(
                    step_id="launch_ide",
                    capability_id="com.nova.desktop.process",
                    action="launch_process",
                    parameters={"executable": "code.exe"},
                    dependencies=[]
                ))
            else:
                logger.info("Planner: IDE is already running in World Model. Skipping launch step.")
                
            # Check if Browser is running
            browser_apps = [e for e in world.get_entities_by_type("Application") if "chrome" in e.attributes.get("name", "").lower() or "msedge" in e.attributes.get("name", "").lower()]
            if not browser_apps:
                steps.append(PlanStep(
                    step_id="launch_browser",
                    capability_id="com.nova.desktop.process",
                    action="launch_process",
                    parameters={"executable": "chrome.exe"},
                    dependencies=[]
                ))
            else:
                logger.info("Planner: Browser is already running in World Model. Skipping launch step.")
                
            if not steps:
                logger.info("Planner: Workspace is already prepared. No steps needed.")
                
            return ExecutionPlan(
                intent=goal.raw_intent,
                strategy=ExecutionStrategy.PARALLEL,
                steps=steps
            )
            
        raise ValueError(f"RuleBasedPlanner does not understand goal: '{goal.id}'")
