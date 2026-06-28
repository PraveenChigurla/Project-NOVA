"""
Project NOVA - Windows Desktop Provider Demonstration.
Demonstrates the Engine safely opening Notepad via the Desktop Provider.
"""

import asyncio
import logging
import sys

from nova.core.config import NovaConfig
from nova.core.kernel import NovaKernel

# Setup logging to see the full orchestration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("nova.demo_desktop")

async def main():
    logger.info("Initializing NOVA Kernel for Desktop Provider Demo...")
    
    config = NovaConfig()
    kernel = NovaKernel(config)
    await kernel.boot()
    
    # -----------------------------------------------------------------
    # Step 1: Planning
    # -----------------------------------------------------------------
    logger.info("\n--- STEP 1: PLANNING ---")
    
    from nova.intelligence.planning.models import ExecutionPlan, PlanStep, ExecutionStrategy
    
    plan = ExecutionPlan(
        intent="Launch Notepad",
        strategy=ExecutionStrategy.SEQUENTIAL,
        steps=[
            PlanStep(
                step_id="launch_notepad",
                capability_id="com.nova.desktop.process",
                action="launch_process",
                parameters={"executable": "notepad.exe"},
                dependencies=[]
            )
        ]
    )
    
    logger.info(f"Generated ExecutionPlan '{plan.plan_id}' with {len(plan.steps)} steps.")

    # -----------------------------------------------------------------
    # Step 2: Grant Permissions
    # -----------------------------------------------------------------
    logger.info("\n--- STEP 2: GRANTING PERMISSIONS ---")
    from nova.security.permissions import PermissionScope
    await kernel.permission_manager.grant("com.nova.desktop.process", PermissionScope.OS_PROCESS_START)
    logger.info("Permission granted for OS_PROCESS_START to com.nova.desktop.process")

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
        if step_res.error:
            logger.error(f"     Error: {step_res.error}")

    # -----------------------------------------------------------------
    # Teardown
    # -----------------------------------------------------------------
    logger.info("\n--- SHUTTING DOWN ---")
    # Notepad might stay open as a detached process depending on how Popen handles it, 
    # but the framework shuts down.
    await kernel.shutdown()

if __name__ == "__main__":
    import os
    if os.name != 'nt':
        logger.error("This demonstration requires a Windows Operating System.")
        sys.exit(1)
        
    asyncio.run(main())
