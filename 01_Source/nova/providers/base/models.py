"""
Provider Framework Models.
Defines the strict schema for external API and hardware integrations.
"""

from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid

def _generate_id() -> str:
    return str(uuid.uuid4())

def _now() -> datetime:
    return datetime.now(timezone.utc)

class ProviderType(str, Enum):
    """Types of providers supported by the framework."""
    DESKTOP = "desktop"
    BROWSER = "browser"
    OCR = "ocr"
    SPEECH = "speech"
    VISION = "vision"
    LLM = "llm"
    STORAGE = "storage"
    NETWORK = "network"
    MOCK = "mock"

class ProviderState(str, Enum):
    """The strict lifecycle state machine for providers."""
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

class ProviderMetadata(BaseModel):
    """Immutable metadata defining a provider."""
    id: str = Field(..., description="Unique identifier (e.g., 'com.nova.provider.mock')")
    name: str = Field(..., description="Human-readable name")
    version: str = Field(..., description="Semantic version string")
    type: ProviderType = Field(..., description="The category of provider")
    description: str = Field(..., description="Brief description of responsibilities")
    author: Optional[str] = Field(None, description="Author or team name")
    
    class Config:
        frozen = True

class ProviderContext(BaseModel):
    """Immutable execution context."""
    trace_id: str = Field(..., description="Unique ID tracking the workflow")
    correlation_id: Optional[str] = Field(None)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        frozen = True

class ProviderRequest(BaseModel):
    """Immutable request payload sent to a provider."""
    id: str = Field(default_factory=_generate_id)
    provider_id: str = Field(...)
    action: str = Field(...)
    payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=_now)
    
    class Config:
        frozen = True

class ProviderResponse(BaseModel):
    """Immutable response payload returned by a provider."""
    request_id: str = Field(...)
    provider_id: str = Field(...)
    success: bool = Field(...)
    data: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[Dict[str, Any]] = Field(None)
    timestamp: datetime = Field(default_factory=_now)
    elapsed_ms: float = Field(...)
    
    class Config:
        frozen = True

class ProviderError(BaseModel):
    """Immutable representation of a provider-level error."""
    error_code: str = Field(...)
    provider_id: Optional[str] = Field(None)
    message: str = Field(...)
    recoverable: bool = Field(False)
    stack_trace: Optional[str] = Field(None)
    
    class Config:
        frozen = True

class ProviderHealth(BaseModel):
    """Immutable health status payload."""
    provider_id: str = Field(...)
    state: ProviderState = Field(...)
    is_healthy: bool = Field(...)
    message: str = Field(default="OK")
    last_heartbeat: datetime = Field(default_factory=_now)
    
    class Config:
        frozen = True
