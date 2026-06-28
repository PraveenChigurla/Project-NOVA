"""
Permission Framework Models.
Defines the strict schema for evaluating and granting capabilities access to providers.
"""

from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime, timezone

def _now() -> datetime:
    return datetime.now(timezone.utc)

class PermissionDecision(str, Enum):
    """The outcome of a permission evaluation."""
    ALLOW = "allow"
    DENY = "deny"
    PROMPT = "prompt"

class PermissionScope(str, Enum):
    """
    The strictly typed scopes that a capability can request.
    This prevents arbitrary string injections.
    """
    OS_FILES_READ = "os.files.read"
    OS_FILES_WRITE = "os.files.write"
    OS_FILES_DELETE = "os.files.delete"
    
    OS_PROCESS_START = "os.process.start"
    OS_PROCESS_KILL = "os.process.kill"
    
    OS_WINDOW_FOCUS = "os.window.focus"
    OS_WINDOW_CAPTURE = "os.window.capture"
    
    OS_MOUSE_MOVE = "os.mouse.move"
    OS_MOUSE_CLICK = "os.mouse.click"
    OS_KEYBOARD_TYPE = "os.keyboard.type"
    
    BROWSER_NAVIGATE = "browser.navigate"
    BROWSER_DOWNLOAD = "browser.download"
    BROWSER_UPLOAD = "browser.upload"
    
    NETWORK_HTTP = "network.http"
    NETWORK_WEBSOCKET = "network.websocket"
    
    FUTURE_AI_REMOTE = "future.ai.remote"

class PermissionRequest(BaseModel):
    """
    An immutable request made by a Capability to access a Provider scope.
    """
    capability_id: str = Field(..., description="The ID of the requesting capability")
    scope: PermissionScope = Field(..., description="The requested permission scope")
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional context for evaluation (e.g. file path)")
    
    class Config:
        frozen = True

class PermissionResult(BaseModel):
    """
    An immutable authorization decision returned by the Permission Manager.
    """
    decision: PermissionDecision = Field(..., description="The final authorization decision")
    message: str = Field(..., description="Audit message explaining the decision")
    expires_at: Optional[datetime] = Field(None, description="If set, this grant is temporary and expires at this UTC time")
    
    @property
    def is_allowed(self) -> bool:
        if self.decision != PermissionDecision.ALLOW:
            return False
        if self.expires_at and self.expires_at < _now():
            return False
        return True
        
    class Config:
        frozen = True
