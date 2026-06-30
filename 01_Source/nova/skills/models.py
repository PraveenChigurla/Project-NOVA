"""
Skill Runtime Models.
Defines schemas for portable Skill Packages.
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class SkillParameter(BaseModel):
    """Definition of an input parameter a Skill accepts."""
    type: str = Field(..., description="Type of the parameter (e.g., string, secret, int).")
    description: Optional[str] = None
    default: Optional[Any] = None

class SkillManifest(BaseModel):
    """
    Representation of `skill.yaml`.
    Defines the declarative metadata and requirements for a Skill Package.
    """
    id: str = Field(..., description="Unique identifier for the skill (e.g., github_login).")
    version: str = Field(..., description="Semantic version of the skill.")
    author: str = Field(default="Unknown")
    description: str = Field(default="")
    
    # Security & Infrastructure
    permissions: List[str] = Field(default_factory=list, description="Required PermissionScopes.")
    requires: List[str] = Field(default_factory=list, description="Required Capability IDs.")
    
    # Inputs
    parameters: Dict[str, SkillParameter] = Field(default_factory=dict, description="Expected input parameters.")
    
    # Execution
    entrypoint: str = Field(default="workflow.yaml", description="The primary workflow file to compile.")
    
    # Internal state (not populated from YAML)
    package_path: str = Field(default="", description="Absolute path to the skill directory on disk.")

class SkillContext(BaseModel):
    """Runtime state injected into a Skill during execution."""
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Resolved values for the skill parameters.")
