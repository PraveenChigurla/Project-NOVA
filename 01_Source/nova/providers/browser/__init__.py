"""
Web Automation Provider Package.
"""
from .models import BrowserResult, BrowserSession, BrowserContext, BrowserPage, BrowserLocator, BrowserElement
from .adapters.base import BrowserAdapter
from .adapters.playwright_adapter import PlaywrightAdapter
from .provider import WebAutomationProvider

__all__ = [
    "BrowserResult", "BrowserSession", "BrowserContext", "BrowserPage", 
    "BrowserLocator", "BrowserElement",
    "BrowserAdapter", "PlaywrightAdapter", 
    "WebAutomationProvider"
]
