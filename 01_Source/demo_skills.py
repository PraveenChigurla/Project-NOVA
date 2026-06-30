"""
Project NOVA - Skill Runtime Demonstration.
Proves that NOVA can dynamically load, compile, and execute declarative YAML skills.
"""

import asyncio
import logging
import sys
import subprocess
import os

from nova.core.config import NovaConfig
from nova.core.kernel import NovaKernel
from nova.skills.compiler import WorkflowCompiler
from nova.skills.models import SkillContext

from nova.providers.desktop.keyboard_provider import KeyboardProvider
from nova.providers.base import ProviderMetadata, ProviderType
from nova.capabilities.desktop.keyboard import KeyboardCapability
from nova.capabilities.base import CapabilityMetadata, CapabilityType
from nova.security.permissions.models import PermissionScope

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("nova.demo_skills")

async def main():
    logger.info("Initializing NOVA Kernel...")
    config = NovaConfig()
    kernel = NovaKernel(config)
    await kernel.boot()
    
    # 1. Register base dependencies for the skill (Keyboard)
    keyboard_provider = KeyboardProvider(ProviderMetadata(
        id="com.nova.provider.keyboard", name="Keyboard Provider", version="1.0.0", type=ProviderType.DESKTOP
    ))
    kernel.provider_registry.register(keyboard_provider)
    await keyboard_provider.start()
    
    keyboard_cap = KeyboardCapability(CapabilityMetadata(
        id="com.nova.desktop.keyboard", name="Keyboard Capability", version="1.0.0", type=CapabilityType.EXECUTION
    ))
    # We must explicitly attach the kernel for capabilities created manually outside discovery
    keyboard_cap.kernel = kernel
    kernel.capability_registry.register(keyboard_cap)
    
    await kernel.permission_manager.grant("com.nova.desktop.keyboard", PermissionScope.OS_KEYBOARD_PRESS)
    
    # 2. Discover and Load Skills
    skills_dir = os.path.join(os.path.dirname(__file__), "skills")
    logger.info(f"Loading skills from {skills_dir} ...")
    loaded = kernel.skill_loader.discover_and_load(skills_dir)
    
    if loaded == 0:
        logger.error("No skills found! Did you create the 'hello' skill?")
        await kernel.shutdown()
        return
        
    hello_skill = kernel.skill_registry.get("hello_world")
    logger.info(f"Loaded Skill: {hello_skill.id} v{hello_skill.version} by {hello_skill.author}")
    
    # 3. Simulate Planner compiling the workflow with parameters
    logger.info("Compiling Workflow with parameters...")
    context = SkillContext(parameters={"name": "Praveen"})
    compiler = WorkflowCompiler()
    
    plan = compiler.compile(hello_skill, context)
    
    # 4. Open Notepad (Target application)
    logger.info("Launching Notepad...")
    proc = subprocess.Popen("notepad.exe")
    await asyncio.sleep(2.0)
    
    # 5. Execute compiled plan
    logger.info("\n>>> EXECUTING SKILL PLAN <<<")
    result = await kernel.execution_engine.execute_plan(plan)
    
    if result.success:
        logger.info("\nSkill Execution Complete.")
    else:
        logger.error(f"Skill Execution Failed: {result.errors}")
        
    logger.info("Closing Notepad in 3 seconds...")
    await asyncio.sleep(3.0)
    proc.kill()
    
    await kernel.shutdown()

if __name__ == "__main__":
    if sys.platform != 'win32':
        logger.error("This demonstration requires Windows.")
        sys.exit(1)
    asyncio.run(main())
