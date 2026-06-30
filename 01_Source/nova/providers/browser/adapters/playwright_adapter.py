"""
Playwright Adapter.
Implements the BrowserAdapter interface using Microsoft Playwright.
"""
import logging
from typing import Optional
from playwright.async_api import async_playwright, Playwright, Browser, BrowserContext, Page

from nova.providers.browser.adapters.base import BrowserAdapter
from nova.providers.browser.models import BrowserResult

logger = logging.getLogger(__name__)

class PlaywrightAdapter(BrowserAdapter):
    """Playwright-backed implementation of the web automation engine."""
    
    def __init__(self):
        self._playwright_mgr = None
        self._playwright: Optional[Playwright] = None
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        self._active_page: Optional[Page] = None
        
    async def initialize(self) -> None:
        logger.info("Initializing Playwright Adapter...")
        self._playwright_mgr = async_playwright()
        self._playwright = await self._playwright_mgr.start()
        
    async def launch(self, headless: bool = False) -> BrowserResult:
        try:
            if not self._playwright:
                await self.initialize()
                
            self._browser = await self._playwright.chromium.launch(headless=headless)
            logger.debug(f"Launched Playwright Chromium (headless={headless})")
            return BrowserResult(success=True, data={"engine": "chromium"})
        except Exception as e:
            logger.error(f"Failed to launch browser: {e}")
            return BrowserResult(success=False, error=str(e))
            
    async def new_context(self, incognito: bool = True) -> BrowserResult:
        try:
            if not self._browser:
                return BrowserResult(success=False, error="Browser not launched.")
                
            self._context = await self._browser.new_context()
            self._active_page = await self._context.new_page()
            logger.debug("Created new Playwright context and active page.")
            return BrowserResult(success=True)
        except Exception as e:
            return BrowserResult(success=False, error=str(e))
            
    async def navigate(self, url: str) -> BrowserResult:
        try:
            if not self._active_page:
                return BrowserResult(success=False, error="No active page available.")
                
            response = await self._active_page.goto(url)
            status = response.status if response else 0
            logger.info(f"Navigated to {url} [Status: {status}]")
            return BrowserResult(success=True, data={"url": url, "status": status})
        except Exception as e:
            return BrowserResult(success=False, error=str(e))
            
    async def click(self, selector: str, strategy: str = "css") -> BrowserResult:
        try:
            if not self._active_page:
                return BrowserResult(success=False, error="No active page available.")
                
            await self._active_page.click(selector)
            return BrowserResult(success=True, data={"selector": selector})
        except Exception as e:
            return BrowserResult(success=False, error=str(e))
            
    async def fill(self, selector: str, value: str, strategy: str = "css") -> BrowserResult:
        try:
            if not self._active_page:
                return BrowserResult(success=False, error="No active page available.")
                
            await self._active_page.fill(selector, value)
            return BrowserResult(success=True, data={"selector": selector})
        except Exception as e:
            return BrowserResult(success=False, error=str(e))
            
    async def screenshot(self, path: str) -> BrowserResult:
        try:
            if not self._active_page:
                return BrowserResult(success=False, error="No active page available.")
                
            await self._active_page.screenshot(path=path)
            logger.debug(f"Saved screenshot to {path}")
            return BrowserResult(success=True, data={"path": path})
        except Exception as e:
            return BrowserResult(success=False, error=str(e))
            
    async def get_title(self) -> BrowserResult:
        try:
            if not self._active_page:
                return BrowserResult(success=False, error="No active page available.")
                
            title = await self._active_page.title()
            return BrowserResult(success=True, data={"title": title})
        except Exception as e:
            return BrowserResult(success=False, error=str(e))
            
    async def close(self) -> None:
        logger.info("Closing Playwright Adapter...")
        if self._context:
            await self._context.close()
        if self._browser:
            await self._browser.close()
        if self._playwright_mgr:
            await self._playwright_mgr.__aexit__()
