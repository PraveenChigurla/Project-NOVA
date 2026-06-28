"""
Project NOVA - Minimal End-to-End Demonstration.
Proves the Kernel and Capability Framework function together.
"""

import asyncio
import logging
import sys

from nova.core.config import NovaConfig
from nova.core.kernel import NovaKernel
from nova.capabilities.base import CapabilityRequest

# Setup basic logging to see the output
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("nova.main")

async def main():
    logger.info("Initializing NOVA...")
    
    # 1. Boot Kernel (which loads Registry and Discovery)
    config = NovaConfig()
    kernel = NovaKernel(config)
    
    # Run the kernel boot sequence
    await kernel.boot()
    
    # 2. Fetch the MockProvider from the Registry
    mock_prov = await kernel.provider_registry.get("com.nova.provider.mock")
    if not mock_prov:
        logger.error("MockProvider not found in registry!")
    else:
        logger.info("--- TRIGGERING PROVIDER EXECUTION ---")
        from nova.providers.base import ProviderRequest
        prov_request = ProviderRequest(
            provider_id="com.nova.provider.mock",
            action="ping"
        )
        prov_response = await mock_prov.run(prov_request)
        logger.info(f"Provider Success: {prov_response.success}")
        logger.info(f"Provider Data: {prov_response.data}")
    
    # 3. Fetch the HelloCapability from the Registry
    hello_cap = await kernel.registry.get("com.nova.hello")
    if not hello_cap:
        logger.error("HelloCapability not found in registry!")
        await kernel.shutdown()
        return

    # 4. Execute an action through the capability (Blocked by Permissions)
    logger.info("--- TRIGGERING CAPABILITY EXECUTION (WITHOUT PERMISSION) ---")
    request = CapabilityRequest(
        capability_id="com.nova.hello",
        action="read_file",
        payload={"path": "C:/test.txt"}
    )
    
    response = await hello_cap.run(request)
    logger.info(f"Response (Should Fail): {response.success}, Error: {response.error}")
    
    # 4. Grant permission and try again
    logger.info("--- GRANTING PERMISSION ---")
    from nova.security.permissions import PermissionScope
    await kernel.permission_manager.grant("com.nova.hello", PermissionScope.OS_FILES_READ)
    
    logger.info("--- TRIGGERING EXECUTION (WITH PERMISSION) ---")
    response_success = await hello_cap.run(request)
    
    logger.info("--- EXECUTION RESPONSE ---")
    logger.info(f"Success: {response_success.success}")
    logger.info(f"Data: {response_success.data}")
    logger.info(f"Elapsed: {response_success.elapsed_ms:.2f}ms")
    
    # 5. Gracefully shutdown the kernel (which shuts down capabilities)
    logger.info("--- TRIGGERING SHUTDOWN ---")
    await kernel.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
