"""
Capability Request Models.
Defines the standard execution payload dispatched to a capability.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid

def _generate_id() -> str:
    return str(uuid.uuid4())

def _now() -> datetime:
    return datetime.now(timezone.utc)

class CapabilityRequest(BaseModel):
    """
    Immutable request payload sent to a capability.
    """
    id: str = Field(default_factory=_generate_id, description="Unique ID for this specific execution request")
    capability_id: str = Field(..., description="Target Capability ID")
    action: str = Field(..., description="The specific action to perform (e.g., 'capture_screen')")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Action-specific arguments in JSON format")
    timestamp: datetime = Field(default_factory=_now, description="When the request was created")
    
    class Config:
        frozen = True
