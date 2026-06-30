"""
Project NOVA - Planner Demonstration.
Demonstrates the generation of an ExecutionPlan without any system execution.
"""

import asyncio
import logging
import sys
import json

from nova.intelligence.planning import RuleBasedPlanner
from nova.intelligence.planning.graph import TaskGraph

# Setup basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

async def main():
    print("\n" + "="*50)
    print("NOVA INTELLIGENCE: PLANNER DEMONSTRATION")
    print("="*50 + "\n")
    
    planner = RuleBasedPlanner()
    
    # ---------------------------------------------------------
    # Test 1: Simple Sequential Plan
    # ---------------------------------------------------------
    intent_1 = "Open Chrome"
    print(f">> USER INTENT: '{intent_1}'\n")
    
    result_1 = await planner.plan(intent_1)
    
    if result_1.success and result_1.plan:
        print(">> GENERATED EXECUTION PLAN:")
        # Dump the Pydantic model to JSON for clear demonstration
        plan_json = result_1.plan.model_dump_json(indent=2)
        print(plan_json)
    else:
        print(f"Failed to generate plan: {result_1.error_message}")
        
    print("\n" + "-"*50 + "\n")
    
    # ---------------------------------------------------------
    # Test 2: Complex DAG Plan (Parallel Execution)
    # ---------------------------------------------------------
    intent_2 = "Complex Workflow"
    print(f">> USER INTENT: '{intent_2}'\n")
    
    result_2 = await planner.plan(intent_2)
    
    if result_2.success and result_2.plan:
        print(f">> PLAN '{result_2.plan.plan_id}' GENERATED.")
        print(">> COMPUTING PARALLEL EXECUTION LAYERS...")
        
        graph = TaskGraph(result_2.plan.steps)
        layers = graph.get_execution_layers()
        
        for idx, layer in enumerate(layers):
            print(f"\nLayer {idx + 1} (Execute in Parallel):")
            for step in layer:
                print(f"  -> [Step: {step.step_id}] Capability: {step.capability_id} | Action: {step.action}")
                
    else:
        print(f"Failed to generate plan: {result_2.error_message}")

    print("\n" + "="*50)
    print("DEMONSTRATION COMPLETE. NO OS EXECUTION OCCURRED.")
    print("="*50 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
