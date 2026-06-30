"""
Tests for the Web Automation Provider Framework.
"""
import pytest
from typing import Dict, Any
from nova.providers.base import ProviderRequest, ProviderMetadata, ProviderType
from nova.providers.browser.provider import WebAutomationProvider
from nova.providers.browser.adapters.base import BrowserAdapter
from nova.providers.browser.models import BrowserResult

class MockAdapter(BrowserAdapter):
    """A dummy adapter for unit testing routing logic."""
    async def initialize(self) -> None:
        pass
        
    async def launch(self, headless: bool = False) -> BrowserResult:
        return BrowserResult(success=True, data={"launched": True})
        
    async def new_context(self, incognito: bool = True) -> BrowserResult:
        return BrowserResult(success=True)
        
    async def navigate(self, url: str) -> BrowserResult:
        return BrowserResult(success=True, data={"url": url})
        
    async def click(self, selector: str, strategy: str = "css") -> BrowserResult:
        return BrowserResult(success=True, data={"clicked": selector})
        
    async def fill(self, selector: str, value: str, strategy: str = "css") -> BrowserResult:
        return BrowserResult(success=True, data={"filled": selector})
        
    async def screenshot(self, path: str) -> BrowserResult:
        return BrowserResult(success=True, data={"path": path})
        
    async def get_title(self) -> BrowserResult:
        return BrowserResult(success=True, data={"title": "Mock Title"})
        
    async def close(self) -> None:
        pass

@pytest.mark.asyncio
async def test_provider_routes_to_adapter():
    metadata = ProviderMetadata(id="test.provider", name="Test", version="1.0", type=ProviderType.BROWSER)
    adapter = MockAdapter()
    provider = WebAutomationProvider(metadata, adapter)
    
    # Test Launch
    req = ProviderRequest(action="launch")
    res = await provider.execute(req)
    assert res["success"] == True
    assert res["data"]["launched"] == True
    
    # Test Navigate
    req = ProviderRequest(action="navigate", payload={"url": "http://test.com"})
    res = await provider.execute(req)
    assert res["success"] == True
    assert res["data"]["url"] == "http://test.com"
    
    # Test Title
    req = ProviderRequest(action="get_title")
    res = await provider.execute(req)
    assert res["success"] == True
    assert res["data"]["title"] == "Mock Title"
