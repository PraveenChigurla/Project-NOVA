"""
Project NOVA - End-to-End Orchestrator Demonstration (Sprint 8).
Proves the unified pipeline from Raw Input -> Intent -> Planner -> Security -> Capability -> Provider -> OS.
"""

import asyncio
import logging
import sys

from nova.core.config import NovaConfig
from nova.core.kernel import NovaKernel
from nova.security.permissions.models import PermissionScope

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("nova.demo_e2e")

async def main():
    logger.info("Initializing NOVA Kernel...")
    config = NovaConfig()
    kernel = NovaKernel(config)
    await kernel.boot()
    
    # Pre-grant permission for the scenarios
    await kernel.permission_manager.grant("com.nova.desktop.process", PermissionScope.OS_PROCESS_START)
    
    # -----------------------------------------------------------------
    # Scenario 1: Standard Success
    # -----------------------------------------------------------------
    logger.info("\n>>> SCENARIO 1: 'Open Notepad' <<<")
    res1 = await kernel.execute_command("Open Notepad")
    if res1:
        logger.info(f"Scenario 1 Result: Success={res1.success}, Elapsed={res1.total_elapsed_ms:.2f}ms")

    # -----------------------------------------------------------------
    # Scenario 2: Launch Chrome (Or gracefully fail if not in PATH)
    # -----------------------------------------------------------------
    logger.info("\n>>> SCENARIO 2: 'Launch Chrome' <<<")
    res2 = await kernel.execute_command("Launch Chrome")
    if res2:
        logger.info(f"Scenario 2 Result: Success={res2.success}")
        for s in res2.step_results:
            if s.error:
                logger.info(f"  Captured Error Gracefully: {s.error}")

    # -----------------------------------------------------------------
    # Scenario 3: Permission Denied
    # -----------------------------------------------------------------
    logger.info("\n>>> SCENARIO 3: 'Open Notepad' (Permission Denied) <<<")
    # Revoke permission
    kernel.permission_manager._grants.clear() 
    res3 = await kernel.execute_command("Open Notepad")
    if res3:
        logger.info(f"Scenario 3 Result: Success={res3.success}")
        for s in res3.step_results:
            if not s.success:
                logger.info(f"  Security Boundary Held! Error: {s.error}")

    # Restore permission for Scenario 5
    await kernel.permission_manager.grant("com.nova.desktop.process", PermissionScope.OS_PROCESS_START)

    # -----------------------------------------------------------------
    # Scenario 4: Unknown Intent
    # -----------------------------------------------------------------
    logger.info("\n>>> SCENARIO 4: 'Cook dinner' <<<")
    res4 = await kernel.execute_command("Cook dinner")
    logger.info(f"Scenario 4 Result: Pipeline aborted early. Return={res4}")

    # -----------------------------------------------------------------
    # Scenario 5: Capability/Provider Failure
    # -----------------------------------------------------------------
    logger.info("\n>>> SCENARIO 5: 'Launch fake_app' <<<")
    res5 = await kernel.execute_command("Launch fake_app")
    if res5:
        logger.info(f"Scenario 5 Result: Success={res5.success}")
        for s in res5.step_results:
            if not s.success:
                logger.info(f"  Engine caught OS failure: {s.error}")

    logger.info("\nEnd-to-End Orchestration Complete.")
    await kernel.shutdown()

if __name__ == "__main__":
    import os
    if os.name != 'nt':
        logger.error("This demonstration requires a Windows Operating System.")
        sys.exit(1)
        
    asyncio.run(main())
