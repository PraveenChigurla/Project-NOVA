"""
Capability Error Models.
Defines the standardized JSON schema for framework failures.
"""

from typing import Optional
from pydantic import BaseModel, Field

class StructuredError(BaseModel):
    """
    Immutable representation of an error within the Capability Framework.
    Allows the AI Reasoning engine to parse errors predictably.
    """
    error_code: str = Field(..., description="Standardized error code (e.g., 'ERR_CAP_TIMEOUT')")
    capability_id: Optional[str] = Field(None, description="The ID of the capability that failed, if known")
    message: str = Field(..., description="Human-readable error description")
    recoverable: bool = Field(False, description="True if the system can potentially retry or recover from this error")
    stack_trace: Optional[str] = Field(None, description="Raw stack trace string, strictly for debugging")
    
    class Config:
        frozen = True
