"""
Project NOVA - Cognitive Layer Demonstration.
Proves that NOVA can enrich intents with real-world state and context before planning.
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

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("nova.demo_cognition")

async def main():
    logger.info("Initializing Cognitive Pipeline...")
    goal_engine = GoalEngine()
    context_engine = ContextEngine()
    state_engine = StateEngine()
    constraint_engine = ConstraintEngine()
    planner = RuleBasedPlanner()
    
    raw_intent = "Prepare my workday"
    logger.info(f"\n[USER INPUT]: {raw_intent}")
    
    # 1. Goal Engine
    logger.info("\n--- 1. GOAL ENGINE ---")
    goal = goal_engine.normalize(raw_intent)
    
    # 2. Context Engine
    logger.info("\n--- 2. CONTEXT ENGINE ---")
    context = context_engine.capture()
    
    # 3. State Engine
    logger.info("\n--- 3. STATE ENGINE ---")
    state = state_engine.capture()
    logger.info(f"Detected processes: {len(state.active_processes)}")
    
    # 4. Constraint Engine
    logger.info("\n--- 4. CONSTRAINT ENGINE ---")
    # For demo purposes, we can artificially force a weekend constraint to see it adapt
    # context.day_of_week = "Sunday"
    constraints = constraint_engine.evaluate(context, state)
    
    # Package
    package = CognitivePackage(
        goal=goal,
        context=context,
        state=state,
        constraints=constraints
    )
    
    # 5. Planning
    logger.info("\n--- 5. PLANNER ---")
    logger.info("Sending Enriched Cognitive Package to Planner...")
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
