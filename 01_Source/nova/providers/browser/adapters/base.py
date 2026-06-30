"""
Web Automation Adapter Base Interface.
Defines the contract that all underlying automation libraries must fulfill.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from nova.providers.browser.models import BrowserResult

class BrowserAdapter(ABC):
    """Abstract interface for browser automation drivers (e.g. Playwright, CDP)."""
    
    @abstractmethod
    async def initialize(self) -> None:
        """Bootstraps the underlying browser engine."""
        pass
        
    @abstractmethod
    async def launch(self, headless: bool = False) -> BrowserResult:
        """Launches a new browser session."""
        pass
        
    @abstractmethod
    async def new_context(self, incognito: bool = True) -> BrowserResult:
        """Creates an isolated browser context."""
        pass
        
    @abstractmethod
    async def navigate(self, url: str) -> BrowserResult:
        """Navigates the active page to a URL."""
        pass
        
    @abstractmethod
    async def click(self, selector: str, strategy: str = "css") -> BrowserResult:
        """Clicks an element in the DOM."""
        pass
        
    @abstractmethod
    async def fill(self, selector: str, value: str, strategy: str = "css") -> BrowserResult:
        """Fills an input element in the DOM."""
        pass
        
    @abstractmethod
    async def screenshot(self, path: str) -> BrowserResult:
        """Captures a screenshot of the active page."""
        pass
        
    @abstractmethod
    async def get_title(self) -> BrowserResult:
        """Returns the title of the active page."""
        pass
        
    @abstractmethod
    async def close(self) -> None:
        """Gracefully tears down the browser and engine."""
        pass
