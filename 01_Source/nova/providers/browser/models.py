"""
Web Automation Domain Models.
Provides a unified abstraction over browser objects (Session, Context, Page, Element).
"""
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from enum import Enum

class BrowserResult(BaseModel):
    """Generic response object for browser operations."""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None

class BrowserLocator(BaseModel):
    """Abstract representation of an element selector."""
    selector: str
    strategy: str = Field(default="css", description="'css', 'xpath', 'text', 'role'")

class BrowserElement(BaseModel):
    """Abstract representation of a DOM element."""
    tag_name: str
    text: Optional[str] = None
    attributes: Dict[str, str] = Field(default_factory=dict)
    bounding_box: Optional[Dict[str, float]] = None # {x, y, width, height}

class BrowserContext(BaseModel):
    """A distinct browsing session (incognito-like) to isolate cookies/cache."""
    context_id: str
    is_incognito: bool = True

class BrowserPage(BaseModel):
    """A distinct tab or window within a context."""
    page_id: str
    url: str
    title: str

class BrowserSession(BaseModel):
    """The overarching browser instance."""
    session_id: str
    contexts: List[BrowserContext] = Field(default_factory=list)
