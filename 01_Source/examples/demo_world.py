"""
Project NOVA - World Model & Observation Framework Demonstration.
Proves the cognitive loop: Observation -> Cognition -> Planning -> Execution -> Reflection.
"""

import asyncio
import logging
import sys

from nova.intelligence.cognition.engines.goal_engine import GoalEngine
from nova.intelligence.cognition.engines.context_engine import ContextEngine
from nova.intelligence.cognition.engines.constraint_engine import ConstraintEngine
from nova.intelligence.cognition.models import CognitivePackage

from nova.intelligence.planning.planner import RuleBasedPlanner

from nova.intelligence.world.models import WorldGraph
from nova.intelligence.world.chronicle import EventChronicle
from nova.intelligence.world.observation import ObservationEngine
from nova.intelligence.world.reflection import ReflectionEngine

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("nova.demo_world")

async def main():
    logger.info("Initializing World Model & Observation Framework...")
    world_graph = WorldGraph()
    chronicle = EventChronicle()
    
    observation_engine = ObservationEngine(world_graph, chronicle)
    reflection_engine = ReflectionEngine(world_graph, chronicle)
    
    logger.info("\n--- 1. OBSERVATION ---")
    observation_engine.observe_initial_state()
    
    logger.info("\nInitializing Cognitive Pipeline...")
    goal_engine = GoalEngine()
    context_engine = ContextEngine()
    constraint_engine = ConstraintEngine()
    planner = RuleBasedPlanner()
    
    raw_intent = "Prepare my workday"
    logger.info(f"\n[USER INPUT]: {raw_intent}")
    chronicle.record("GoalReceived", {"raw_intent": raw_intent})
    
    # 2. Cognition
    logger.info("\n--- 2. COGNITION ---")
    goal = goal_engine.normalize(raw_intent)
    chronicle.record("GoalNormalized", {"goal_id": goal.id})
    
    context = context_engine.capture()
    constraints = constraint_engine.evaluate(context, world_graph)
    
    # Package
    package = CognitivePackage(
        goal=goal,
        context=context,
        world=world_graph,
        constraints=constraints
    )
    chronicle.record("ContextBuilt")
    
    # 3. Planning
    logger.info("\n--- 3. PLANNING ---")
    logger.info("Planner queries the World Graph to determine the execution plan...")
    result = await planner.plan(package)
    chronicle.record("PlanGenerated", {"success": result.success})
    
    if result.success:
        plan = result.plan
        logger.info(f"\n>>> FINAL EXECUTION PLAN ({plan.strategy.value}) <<<")
        if not plan.steps:
            logger.info("Plan is empty! Why? Because the ObservationEngine seeded the WorldGraph with Chrome and VS Code.")
            chronicle.record("ExecutionStepSkipped", {"reason": "Already present in WorldGraph"})
        for step in plan.steps:
            logger.info(f" - [{step.capability_id}] {step.action} -> {step.parameters}")
            
        # 4. Simulated Execution
        logger.info("\n--- 4. EXECUTION ---")
        logger.info("Executing plan...")
        chronicle.record("ExecutionCompleted")
        
        # 5. Reflection
        logger.info("\n--- 5. REFLECTION ---")
        # Define what we expect the world to look like after execution
        expected_state = {"require_vscode": True}
        reflection_report = reflection_engine.evaluate(goal.id, expected_state)
        
        if reflection_report.memory_suggestions:
            logger.info(f"Reflection Engine Learning Hook: {reflection_report.memory_suggestions}")
            
    else:
        logger.error(f"Planning failed: {result.error_message}")
        
    logger.info("\n--- EVENT CHRONICLE DUMP ---")
    for event in chronicle.get_events():
        logger.info(f"[{event.timestamp:.2f}] {event.event_type} - {event.details}")

if __name__ == "__main__":
    if sys.platform != 'win32':
        logger.error("This demonstration requires Windows.")
        sys.exit(1)
    asyncio.run(main())
