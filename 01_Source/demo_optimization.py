"""
Project NOVA - Optimization Engine Demonstration.
Simulates 100 executions and proves NOVA can generate evidence-based optimization proposals.
"""

import sys
import logging
import random
from nova.intelligence.world.chronicle import EventChronicle
from nova.intelligence.optimization.engine import OptimizationEngine

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("nova.demo_optimization")

def simulate_chronicle_history() -> EventChronicle:
    logger.info("Simulating 100 executions of 'prepare_workspace'...")
    chronicle = EventChronicle()
    
    for i in range(100):
        chronicle.record("GoalReceived", {"goal_id": "prepare_workspace"})
        chronicle.record("PlanGenerated", {"goal_id": "prepare_workspace"})
        
        # In 93% of cases, VS Code is already open and a step gets skipped.
        if random.random() < 0.93:
            chronicle.record("ExecutionStepSkipped", {"goal_id": "prepare_workspace", "reason": "VS Code already running"})
            
        chronicle.record("ExecutionCompleted", {"goal_id": "prepare_workspace"})
        chronicle.record("ReflectionCompleted", {"goal_id": "prepare_workspace"})
        
    logger.info(f"Generated {len(chronicle.get_events())} events in the Chronicle.")
    return chronicle

def main():
    logger.info("Initializing Optimization Engine...")
    
    # 1. Simulate the history
    chronicle = simulate_chronicle_history()
    
    # 2. Initialize Engine
    engine = OptimizationEngine(chronicle)
    
    # 3. Mine the chronicle for optimizations
    logger.info("\n--- MINING CHRONICLE FOR OPTIMIZATIONS ---")
    proposals = engine.generate_proposals()
    
    if not proposals:
        logger.info("No statistically significant optimizations found.")
        return
        
    # 4. Present Proposals
    logger.info("\n>>> OPTIMIZATION PROPOSALS <<<")
    for prop in proposals:
        logger.info(f"\n[PROPOSAL ID: {prop.proposal_id}]")
        logger.info(f"Category: {prop.category.value}")
        logger.info(f"Target: {prop.affected_skill}")
        logger.info(f"Confidence: {prop.confidence:.2%}")
        logger.info(f"Reason: {prop.reason}")
        logger.info(f"Benefit: {prop.expected_benefit}")
        logger.info(f"Risk: {prop.risk}")
        logger.warning(f"Requires Human Approval: {prop.requires_approval}")
        
    logger.info("\nSUCCESS: Optimization Proposals generated based on statistical evidence. Zero runtime modifications made.")

if __name__ == "__main__":
    if sys.platform != 'win32':
        logger.error("This demonstration requires Windows.")
        sys.exit(1)
    main()
