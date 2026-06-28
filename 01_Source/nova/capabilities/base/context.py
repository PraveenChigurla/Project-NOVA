"""
Capability Context Models.
Defines the execution context passed alongside requests.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class CapabilityContext(BaseModel):
    """
    Immutable execution context.
    Provides contextual metadata like tracing IDs and correlation IDs
    that are not part of the functional payload but required for system observability.
    """
    trace_id: str = Field(..., description="Unique ID tracking the entire asynchronous workflow")
    correlation_id: Optional[str] = Field(None, description="ID connecting related workflows together")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional context metadata (e.g., origin_agent_id)")
    
    class Config:
        frozen = True
