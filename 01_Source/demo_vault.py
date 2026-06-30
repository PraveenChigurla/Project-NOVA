"""
Project NOVA - Secret Vault Demonstration.
Proves that NOVA can securely store, retrieve, and inject credentials into Skills without exposing them.
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
from nova.security.vault.models import VaultIdentity, VaultCredential, CredentialType

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

logger = logging.getLogger("nova.demo_vault")

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
    keyboard_cap.kernel = kernel
    kernel.capability_registry.register(keyboard_cap)
    
    await kernel.permission_manager.grant("com.nova.desktop.keyboard", PermissionScope.OS_KEYBOARD_PRESS)
    
    # 2. Setup Vault
    MASTER_PASSWORD = "super_secure_master_password_123!"
    logger.info("Unlocking Secret Vault...")
    kernel.secret_vault.unlock(MASTER_PASSWORD)
    
    # Mock storing an identity
    github_id = VaultIdentity(
        id="github.main",
        description="Praveen's Main GitHub Account",
        credentials={
            "username": VaultCredential(type=CredentialType.USERNAME, value="praveen_nova_admin"),
            "password": VaultCredential(type=CredentialType.PASSWORD, value="hunter2")
        }
    )
    kernel.secret_vault.store(github_id)
    
    # 3. Discover and Load Skills
    skills_dir = os.path.join(os.path.dirname(__file__), "skills")
    logger.info(f"Loading skills from {skills_dir} ...")
    kernel.skill_loader.discover_and_load(skills_dir)
    
    github_skill = kernel.skill_registry.get("github_login")
    if not github_skill:
        logger.error("Failed to load github_login skill.")
        return
        
    logger.info(f"Loaded Skill: {github_skill.id}")
    
    # 4. Compile Workflow (Injects Vault secrets)
    logger.info("Compiling Workflow and requesting Vault secrets...")
    context = SkillContext()
    compiler = WorkflowCompiler()
    
    # The compiler will hit kernel.secret_vault.get_credential() during this step
    plan = compiler.compile(github_skill, context, vault=kernel.secret_vault)
    
    # 5. Open Notepad
    logger.info("Launching Notepad...")
    proc = subprocess.Popen("notepad.exe")
    await asyncio.sleep(2.0)
    
    # 6. Execute compiled plan
    logger.info("\n>>> EXECUTING SKILL PLAN <<<")
    result = await kernel.execution_engine.execute_plan(plan)
    
    if result.success:
        logger.info("\nSkill Execution Complete. Notice how the Audit Log captured the secret access!")
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
