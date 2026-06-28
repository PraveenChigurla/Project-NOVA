"""
Capability Health Models.
Defines the state machine and health status for capabilities.
"""

from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime, timezone

def _now() -> datetime:
    return datetime.now(timezone.utc)

class CapabilityState(str, Enum):
    """
    The exact state machine defined in Sprint 2B.2.
    """
    CREATED = "created"
    REGISTERED = "registered"
    INITIALIZED = "initialized"
    STARTED = "started"
    READY = "ready"
    EXECUTING = "executing"
    IDLE = "idle"
    STOPPING = "stopping"
    STOPPED = "stopped"
    SHUTDOWN = "shutdown"

class CapabilityHealth(BaseModel):
    """
    Immutable health status payload returned during the asynchronous watchdog heartbeat.
    """
    capability_id: str = Field(..., description="The ID of the reporting capability")
    state: CapabilityState = Field(..., description="The current state of the capability")
    is_healthy: bool = Field(..., description="True if the capability is fully operational")
    message: str = Field(default="OK", description="Diagnostic message (e.g., error reason if unhealthy)")
    last_heartbeat: datetime = Field(default_factory=_now, description="When the health check was performed")
    
    class Config:
        frozen = True
