"""
Project NOVA - Execution Engine Demonstration.
Demonstrates the entire lifecycle: Planner -> Engine -> Permission -> Capability.
"""

import asyncio
import logging
import sys

from nova.core.config import NovaConfig
from nova.core.kernel import NovaKernel
from nova.intelligence.planning import RuleBasedPlanner

# Setup logging to see the full orchestration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("nova.demo_execution")

async def main():
    logger.info("Initializing NOVA Kernel for Execution Demo...")
    
    config = NovaConfig()
    kernel = NovaKernel(config)
    await kernel.boot()
    
    # -----------------------------------------------------------------
    # Step 1: Planning
    # -----------------------------------------------------------------
    logger.info("\n--- STEP 1: PLANNING ---")
    planner = RuleBasedPlanner()
    intent = "Open Chrome" # This maps to our mock com.nova.desktop capability in the RuleBasedPlanner
    # Wait, the RuleBasedPlanner uses com.nova.desktop for Open Chrome.
    # But we only have com.nova.hello loaded in the demo.
    # Let's use the 'Hello' capability instead.
    
    from nova.intelligence.planning.models import ExecutionPlan, PlanStep, ExecutionStrategy
    
    # We will build a custom plan targeting the HelloCapability for this demo
    plan = ExecutionPlan(
        intent="Read a file and say hello",
        strategy=ExecutionStrategy.SEQUENTIAL,
        steps=[
            PlanStep(
                step_id="step_read",
                capability_id="com.nova.hello",
                action="read_file",
                parameters={"path": "C:/demo.txt"},
                dependencies=[]
            ),
            PlanStep(
                step_id="step_hello",
                capability_id="com.nova.hello",
                action="say_hello",
                parameters={"name": "Execution Engine"},
                dependencies=["step_read"]
            )
        ]
    )
    
    logger.info(f"Generated ExecutionPlan '{plan.plan_id}' with {len(plan.steps)} steps.")

    # -----------------------------------------------------------------
    # Step 2: Grant Permissions
    # -----------------------------------------------------------------
    logger.info("\n--- STEP 2: GRANTING PERMISSIONS ---")
    from nova.security.permissions import PermissionScope
    # We need to grant OS_FILES_READ so step_read doesn't fail
    await kernel.permission_manager.grant("com.nova.hello", PermissionScope.OS_FILES_READ)
    logger.info("Permission granted for OS_FILES_READ to com.nova.hello")

    # -----------------------------------------------------------------
    # Step 3: Execution
    # -----------------------------------------------------------------
    logger.info("\n--- STEP 3: EXECUTING PLAN ---")
    result = await kernel.execution_engine.execute_plan(plan)
    
    logger.info("\n--- EXECUTION RESULT ---")
    logger.info(f"Success: {result.success}")
    logger.info(f"State: {result.state.value}")
    logger.info(f"Elapsed Time: {result.total_elapsed_ms:.2f}ms")
    
    for step_res in result.step_results:
        logger.info(f"  -> Step '{step_res.step_id}': Success={step_res.success} | Action='{step_res.action}' | Data={step_res.data}")

    # -----------------------------------------------------------------
    # Teardown
    # -----------------------------------------------------------------
    logger.info("\n--- SHUTTING DOWN ---")
    await kernel.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
