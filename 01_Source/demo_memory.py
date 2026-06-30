"""
Project NOVA - Memory Architecture Demonstration.
Proves that NOVA can distinguish between and retrieve Semantic Facts and Historical Episodes during execution.
"""

import asyncio
import logging
import sys

from nova.intelligence.cognition.engines.goal_engine import GoalEngine
from nova.intelligence.cognition.engines.context_engine import ContextEngine
from nova.intelligence.cognition.engines.state_engine import StateEngine
from nova.intelligence.cognition.engines.constraint_engine import ConstraintEngine
from nova.intelligence.cognition.models import CognitivePackage

from nova.intelligence.planning.planner import RuleBasedPlanner

from nova.intelligence.memory.manager import MemoryManager
from nova.intelligence.memory.models import Fact, Episode

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("nova.demo_memory")

async def main():
    logger.info("Initializing Memory Manager...")
    memory_manager = MemoryManager()
    
    # Pre-populate Memory
    logger.info("Storing Semantic Fact: Preferred IDE is VS Code.")
    memory_manager.semantic.store_fact(Fact(key="preferred_ide", value="vscode", confidence=0.99))
    
    logger.info("Storing Historical Episode: Workspace prepared yesterday.")
    memory_manager.episodic.record(Episode(
        goal_id="prepare_workspace",
        success=True,
        summary="Prepared workspace. Launched VS Code and Chrome successfully."
    ))
    
    logger.info("\nInitializing Cognitive Pipeline...")
    goal_engine = GoalEngine()
    context_engine = ContextEngine()
    state_engine = StateEngine()
    constraint_engine = ConstraintEngine()
    planner = RuleBasedPlanner()
    
    raw_intent = "Prepare my workday"
    logger.info(f"\n[USER INPUT]: {raw_intent}")
    
    # 1. Goal Engine
    goal = goal_engine.normalize(raw_intent)
    
    # 2. Memory Retrieval (The new addition!)
    logger.info("\n--- 2. MEMORY MANAGER ---")
    memory_manager.initialize_session()
    memory_manager.working.set("current_intent", raw_intent)
    memory_snapshot = memory_manager.build_snapshot(current_goal_id=goal.id)
    
    # 3. Context Engine
    context = context_engine.capture()
    
    # 4. State Engine
    state = state_engine.capture()
    
    # 5. Constraint Engine
    constraints = constraint_engine.evaluate(context, state)
    
    # Package
    package = CognitivePackage(
        goal=goal,
        context=context,
        state=state,
        constraints=constraints,
        memory=memory_snapshot
    )
    
    # 6. Planning
    logger.info("\n--- 6. PLANNER ---")
    logger.info("Sending Enriched Cognitive Package (now with Memory) to Planner...")
    result = await planner.plan(package)
    
    if result.success:
        plan = result.plan
        logger.info(f"\n>>> FINAL EXECUTION PLAN ({plan.strategy.value}) <<<")
        for step in plan.steps:
            logger.info(f" - [{step.capability_id}] {step.action} -> {step.parameters}")
    else:
        logger.error(f"Planning failed: {result.error_message}")

if __name__ == "__main__":
    if sys.platform != 'win32':
        logger.error("This demonstration requires Windows.")
        sys.exit(1)
    asyncio.run(main())
