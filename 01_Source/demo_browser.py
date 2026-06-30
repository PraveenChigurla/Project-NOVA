"""
Project NOVA - Web Automation Provider Demonstration.
Proves that NOVA can abstract browser automation through the Provider pattern using Playwright.
"""

import asyncio
import logging
import sys
import os

from nova.core.config import NovaConfig
from nova.core.kernel import NovaKernel
from nova.providers.base import ProviderMetadata, ProviderType, ProviderRequest
from nova.providers.browser.provider import WebAutomationProvider
from nova.providers.browser.adapters.playwright_adapter import PlaywrightAdapter

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("nova.demo_browser")

async def main():
    logger.info("Initializing NOVA Kernel...")
    config = NovaConfig()
    kernel = NovaKernel(config)
    await kernel.boot()
    
    # 1. Instantiate the Playwright Adapter
    adapter = PlaywrightAdapter()
    
    # 2. Register Web Automation Provider
    browser_provider = WebAutomationProvider(
        metadata=ProviderMetadata(
            id="com.nova.provider.web_automation", 
            name="Web Automation Provider", 
            version="1.0.0", 
            type=ProviderType.BROWSER
        ),
        adapter=adapter
    )
    
    kernel.provider_registry.register(browser_provider)
    await browser_provider.initialize()
    await browser_provider.start()
    
    logger.info("\n>>> EXECUTING BROWSER AUTOMATION <<<")
    
    # 3. Launch Browser (Headful so the user can see it)
    logger.info("Launching Chromium...")
    req_launch = ProviderRequest(action="launch", payload={"headless": False})
    res_launch = await browser_provider.execute(req_launch)
    
    if not res_launch.get("success"):
        logger.error(f"Failed to launch browser: {res_launch.get('error')}")
        return
        
    # 4. Navigate
    target_url = "https://example.com"
    logger.info(f"Navigating to {target_url} ...")
    req_nav = ProviderRequest(action="navigate", payload={"url": target_url})
    await browser_provider.execute(req_nav)
    
    # 5. Extract Title
    req_title = ProviderRequest(action="get_title", payload={})
    res_title = await browser_provider.execute(req_title)
    
    if res_title.get("success"):
        logger.info(f"Page Title Extracted: '{res_title['data']['title']}'")
        
    # 6. Capture Screenshot
    screenshot_path = os.path.join(os.path.dirname(__file__), "example_screenshot.png")
    logger.info("Capturing Screenshot...")
    req_img = ProviderRequest(action="screenshot", payload={"path": screenshot_path})
    res_img = await browser_provider.execute(req_img)
    
    if res_img.get("success"):
        logger.info(f"Screenshot saved to: {screenshot_path}")
        
    logger.info("Leaving browser open for 3 seconds...")
    await asyncio.sleep(3.0)
    
    # 7. Cleanup
    await browser_provider.stop()
    await kernel.shutdown()
    logger.info("Demonstration Complete.")

if __name__ == "__main__":
    if sys.platform != 'win32':
        logger.error("This demonstration requires Windows.")
        sys.exit(1)
    asyncio.run(main())
