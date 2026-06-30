"""
Project NOVA - Human Interaction Engine Demonstration.
Proves that NOVA can move the mouse physically and naturally using Bezier streams.
"""

import asyncio
import logging
import sys
import ctypes

from nova.core.config import NovaConfig
from nova.core.kernel import NovaKernel
from nova.providers.desktop.mouse_provider import MouseProvider
from nova.providers.base import ProviderMetadata, ProviderType
from nova.capabilities.desktop.mouse import MouseCapability
from nova.capabilities.base import CapabilityMetadata, CapabilityType
from nova.intelligence.planning.models import ExecutionPlan, PlanStep, ExecutionStrategy
from nova.security.permissions.models import PermissionScope

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("nova.demo_interaction")

async def main():
    logger.info("Initializing NOVA Kernel...")
    config = NovaConfig()
    kernel = NovaKernel(config)
    await kernel.boot()
    
    # 1. Register Mouse Provider
    mouse_provider = MouseProvider(ProviderMetadata(
        id="com.nova.provider.mouse",
        name="Mouse Provider",
        version="1.0.0",
        type=ProviderType.DESKTOP
    ))
    kernel.provider_registry.register(mouse_provider)
    await mouse_provider.initialize()
    await mouse_provider.start()
    
    # 2. Register Mouse Capability
    mouse_cap = MouseCapability(CapabilityMetadata(
        id="com.nova.desktop.mouse",
        name="Mouse Capability",
        version="1.0.0",
        type=CapabilityType.EXECUTION
    ))
    kernel.capability_registry.register(mouse_cap)
    
    # 3. Grant OS_MOUSE Permissions
    logger.info("Granting Mouse Permissions...")
    await kernel.permission_manager.grant("com.nova.desktop.mouse", PermissionScope.OS_MOUSE_MOVE)
    await kernel.permission_manager.grant("com.nova.desktop.mouse", PermissionScope.OS_MOUSE_CLICK)
    
    # 4. Fetch screen resolution dynamically using ctypes
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    
    target_x = int(screen_width * 0.75)
    target_y = int(screen_height * 0.25)
    
    logger.info(f"Target Acquired at [{target_x}, {target_y}]")
    
    # 5. Create Execution Plan
    plan = ExecutionPlan(
        intent="Click Target Naturally",
        strategy=ExecutionStrategy.SEQUENTIAL,
        steps=[
            PlanStep(
                step_id="step_1",
                capability_id="com.nova.desktop.mouse",
                action="click_human",
                parameters={"x": target_x, "y": target_y, "profile": "natural", "button": "left"},
                dependencies=[]
            )
        ]
    )
    
    logger.info("\n>>> EXECUTING BEZIER STREAM <<<")
    logger.info("Please watch your cursor physically move across the screen.")
    logger.info("Starting in 3 seconds...")
    await asyncio.sleep(3)
    
    result = await kernel.execution_engine.execute_plan(plan)
    
    if result.success:
        logger.info("\nInteraction complete. Notice the ease-in, hover delay, and ease-out.")
    else:
        logger.error(f"Interaction failed: {result.errors}")
        
    await kernel.shutdown()

if __name__ == "__main__":
    if sys.platform != 'win32':
        logger.error("This demonstration requires Windows.")
        sys.exit(1)
    asyncio.run(main())
