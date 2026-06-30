"""
Project NOVA - LLM Integration Layer Demonstration.
Proves that the LLM acts as a stateless advisor, returning structured GoalContracts to the deterministic runtime.
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
from nova.intelligence.memory.manager import MemoryManager
from nova.intelligence.memory.models import Fact

from nova.intelligence.llm.manager import LLMManager
from nova.intelligence.llm.engines.router import ModelRouter
from nova.intelligence.llm.adapters.mock_adapter import MockLLMAdapter

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("nova.demo_llm")

async def main():
    logger.info("Initializing Architecture...")
    world_graph = WorldGraph()
    memory_manager = MemoryManager()
    
    # Pre-populate Memory to prove Context Assembly
    memory_manager.semantic.store_fact(Fact(key="preferred_ide", value="vscode", confidence=0.99))
    
    # LLM Initialization
    mock_provider = MockLLMAdapter()
    router = ModelRouter(default_provider=mock_provider)
    llm_manager = LLMManager(router=router)
    
    goal_engine = GoalEngine()
    context_engine = ContextEngine()
    constraint_engine = ConstraintEngine()
    planner = RuleBasedPlanner()
    
    raw_intent = "Prepare my workday"
    logger.info(f"\n[USER INPUT]: {raw_intent}")
    
    # 1. LLM Integration Layer (The new addition!)
    logger.info("\n--- 1. LLM COGNITIVE ADVISOR ---")
    memory_snapshot = memory_manager.build_snapshot(current_goal_id="unknown") # Pre-goal context
    
    # The LLM takes the intent, memory, and world state, and returns a strict Contract
    goal_contract = llm_manager.interpret_intent(raw_intent, world_graph, memory_snapshot)
    
    # Safety Check
    if goal_contract.requires_confirmation:
        logger.warning(f"LLM flagged intent for confirmation: {goal_contract.safety_flags}")
        # In a real app, we would pause here and ask the user.
    
    # 2. Cognition (Deterministic)
    logger.info("\n--- 2. DETERMINISTIC COGNITION ---")
    # The Goal Engine now just unpacks the LLM contract
    goal = goal_engine.normalize(goal_contract, raw_intent)
    
    context = context_engine.capture()
    constraints = constraint_engine.evaluate(context, world_graph)
    
    # Package
    package = CognitivePackage(
        goal=goal,
        context=context,
        world=world_graph,
        constraints=constraints,
        memory=memory_snapshot
    )
    
    # 3. Planning
    logger.info("\n--- 3. PLANNING ---")
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
