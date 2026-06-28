"""
Capability Metadata Models.
Defines the strict manifest schema required for capability registration.
"""

from typing import List, Optional
from pydantic import BaseModel, Field

class CapabilityMetadata(BaseModel):
    """
    Immutable metadata defining a capability.
    Used by the Registry to validate manifests before loading code.
    """
    id: str = Field(..., description="Unique identifier for the capability (e.g., 'com.nova.vision')")
    name: str = Field(..., description="Human-readable name")
    version: str = Field(..., description="Semantic version string")
    description: str = Field(..., description="Brief description of responsibilities")
    permissions_required: List[str] = Field(default_factory=list, description="List of OS-level required permissions")
    dependencies: List[str] = Field(default_factory=list, description="List of Capability IDs required to run")
    tags: List[str] = Field(default_factory=list, description="Categorical tags for discovery")
    supported_intents: List[str] = Field(default_factory=list, description="List of AI intents this capability handles")
    author: Optional[str] = Field(None, description="Author or team name")
    
    class Config:
        frozen = True
