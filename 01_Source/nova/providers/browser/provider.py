"""
Web Automation Provider.
Exposes a unified browser automation API using dependency-injected Adapters.
"""
import logging
from typing import Dict, Any, Optional

from nova.providers.base import Provider, ProviderRequest, ProviderContext, ProviderMetadata, ProviderType
from nova.providers.browser.adapters.base import BrowserAdapter
from nova.providers.browser.models import BrowserResult

logger = logging.getLogger(__name__)

class WebAutomationProvider(Provider):
    """
    High-level browser automation controller. 
    Routes requests to the underlying Adapter (e.g. Playwright).
    """
    
    def __init__(self, metadata: ProviderMetadata, adapter: BrowserAdapter):
        super().__init__(metadata)
        self.adapter = adapter
            
    async def initialize(self) -> None:
        logger.info(f"[{self.metadata.id}] Initializing Web Automation Provider...")
        await self.adapter.initialize()
        
    async def start(self) -> None:
        logger.info(f"[{self.metadata.id}] Web Automation Provider Online.")
        
    async def execute(self, request: ProviderRequest, context: Optional[ProviderContext] = None) -> Dict[str, Any]:
        logger.debug(f"[{self.metadata.id}] Action: {request.action}")
        
        result = BrowserResult(success=False, error="Unknown action")
        
        if request.action == "launch":
            headless = request.payload.get("headless", False)
            result = await self.adapter.launch(headless)
            if result.success:
                await self.adapter.new_context()
                
        elif request.action == "navigate":
            url = request.payload.get("url")
            if url:
                result = await self.adapter.navigate(url)
                
        elif request.action == "get_title":
            result = await self.adapter.get_title()
            
        elif request.action == "screenshot":
            path = request.payload.get("path", "screenshot.png")
            result = await self.adapter.screenshot(path)
            
        elif request.action == "click":
            selector = request.payload.get("selector")
            if selector:
                result = await self.adapter.click(selector)
                
        elif request.action == "fill":
            selector = request.payload.get("selector")
            value = request.payload.get("value", "")
            if selector:
                result = await self.adapter.fill(selector, value)
                
        else:
            raise ValueError(f"WebAutomationProvider does not support action: '{request.action}'")

        return result.model_dump()

    async def stop(self) -> None:
        await self.adapter.close()
        
    async def shutdown(self) -> None:
        pass
