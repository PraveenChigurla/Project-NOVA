"""
Project NOVA - Keyboard Provider Demonstration.
Proves that NOVA can type text naturally with variable speeds using SendInput.
"""

import asyncio
import logging
import sys
import subprocess

from nova.core.config import NovaConfig
from nova.core.kernel import NovaKernel
from nova.providers.desktop.keyboard_provider import KeyboardProvider
from nova.providers.base import ProviderMetadata, ProviderType
from nova.capabilities.desktop.keyboard import KeyboardCapability
from nova.capabilities.base import CapabilityMetadata, CapabilityType
from nova.intelligence.planning.models import ExecutionPlan, PlanStep, ExecutionStrategy
from nova.security.permissions.models import PermissionScope

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("nova.demo_keyboard")

async def main():
    logger.info("Initializing NOVA Kernel...")
    config = NovaConfig()
    kernel = NovaKernel(config)
    await kernel.boot()
    
    # 1. Register Keyboard Provider
    keyboard_provider = KeyboardProvider(ProviderMetadata(
        id="com.nova.provider.keyboard",
        name="Keyboard Provider",
        version="1.0.0",
        type=ProviderType.DESKTOP
    ))
    kernel.provider_registry.register(keyboard_provider)
    await keyboard_provider.initialize()
    await keyboard_provider.start()
    
    # 2. Register Keyboard Capability
    keyboard_cap = KeyboardCapability(CapabilityMetadata(
        id="com.nova.desktop.keyboard",
        name="Keyboard Capability",
        version="1.0.0",
        type=CapabilityType.EXECUTION
    ))
    kernel.capability_registry.register(keyboard_cap)
    
    # 3. Grant OS_KEYBOARD Permissions
    logger.info("Granting Keyboard Permissions...")
    await kernel.permission_manager.grant("com.nova.desktop.keyboard", PermissionScope.OS_KEYBOARD_PRESS)
    
    # 4. Open Notepad (Target application)
    logger.info("Launching Notepad...")
    proc = subprocess.Popen("notepad.exe")
    await asyncio.sleep(2.0) # Wait for it to open and focus
    
    # 5. Create Execution Plan
    plan = ExecutionPlan(
        intent="Type Text Naturally",
        strategy=ExecutionStrategy.SEQUENTIAL,
        steps=[
            PlanStep(
                step_id="step_1",
                capability_id="com.nova.desktop.keyboard",
                action="type_human",
                parameters={"text": "Hello from Project NOVA! (Typed seamlessly with native Unicode support)", "profile": "natural"},
                dependencies=[]
            )
        ]
    )
    
    logger.info("\n>>> EXECUTING TYPING STREAM <<<")
    logger.info("Watch Notepad closely...")
    
    result = await kernel.execution_engine.execute_plan(plan)
    
    if result.success:
        logger.info("\nInteraction complete. Notice the natural delays between keystrokes.")
    else:
        logger.error(f"Interaction failed: {result.errors}")
        
    logger.info("Closing Notepad in 3 seconds...")
    await asyncio.sleep(3.0)
    proc.kill()
    
    await kernel.shutdown()

if __name__ == "__main__":
    if sys.platform != 'win32':
        logger.error("This demonstration requires Windows.")
        sys.exit(1)
    asyncio.run(main())
