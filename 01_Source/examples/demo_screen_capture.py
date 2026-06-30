"""
Project NOVA - Screen Capture Provider Demonstration.
Demonstrates the Engine safely requesting and receiving a screenshot via the Vision Provider.
"""

import asyncio
import logging
import sys

from nova.core.config import NovaConfig
from nova.core.kernel import NovaKernel

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("nova.demo_screen_capture")

async def main():
    logger.info("Initializing NOVA Kernel for Screen Capture Demo...")
    config = NovaConfig()
    kernel = NovaKernel(config)
    await kernel.boot()
    
    # We will build a manual ExecutionPlan to skip the NLP Intent step
    # since we just want to test the Capability -> Provider link.
    from nova.intelligence.planning.models import ExecutionPlan, PlanStep, ExecutionStrategy
    from nova.security.permissions.models import PermissionScope
    
    plan = ExecutionPlan(
        intent="Capture Active Monitor",
        strategy=ExecutionStrategy.SEQUENTIAL,
        steps=[
            PlanStep(
                step_id="capture_monitor_step",
                capability_id="com.nova.vision.screen",
                action="capture_active_monitor",
                parameters={},
                dependencies=[]
            )
        ]
    )
    
    # Grant permission
    logger.info("Granting Permission: OS_WINDOW_CAPTURE")
    await kernel.permission_manager.grant("com.nova.vision.screen", PermissionScope.OS_WINDOW_CAPTURE)
    
    # Execute Plan
    logger.info("Executing Plan...")
    result = await kernel.execution_engine.execute_plan(plan)
    
    if result.success:
        for step in result.step_results:
            logger.info(f"Capture Success!")
            logger.info(f"Resolution: {step.data.get('resolution')}")
            logger.info(f"Image saved to: {step.data.get('image_path')}")
    else:
        logger.error("Execution failed!")
        for step in result.step_results:
            if step.error:
                logger.error(step.error)
                
    await kernel.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
