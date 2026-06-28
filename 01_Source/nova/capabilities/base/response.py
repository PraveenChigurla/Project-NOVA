"""
Capability Response Models.
Defines the standard execution result returned by a capability.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid

def _now() -> datetime:
    return datetime.now(timezone.utc)

class CapabilityResponse(BaseModel):
    """
    Immutable response payload returned by a capability.
    """
    request_id: str = Field(..., description="The ID of the request that triggered this response")
    capability_id: str = Field(..., description="The ID of the capability returning the response")
    success: bool = Field(..., description="True if the action completed successfully")
    data: Dict[str, Any] = Field(default_factory=dict, description="Result payload in JSON format")
    error: Optional[Dict[str, Any]] = Field(None, description="Error details if success is False")
    timestamp: datetime = Field(default_factory=_now, description="When the response was created")
    elapsed_ms: float = Field(..., description="Execution time in milliseconds")
    
    class Config:
        frozen = True
