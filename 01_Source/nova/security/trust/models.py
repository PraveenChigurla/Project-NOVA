"""
Trust Framework Models.
"""
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class PolicyEnvironment(str, Enum):
    PERSONAL = "personal"
    ENTERPRISE = "enterprise"
    STRICT = "strict"

class PackageManifest(BaseModel):
    """Represents the parsed metadata of a .nova package."""
    name: str
    version: str
    publisher: str
    permissions_requested: List[str] = Field(default_factory=list)
    has_signature: bool = False
    has_sbom: bool = False

class TrustEvaluation(BaseModel):
    """The result of the Trust Framework's analysis."""
    is_trusted: bool
    reasons: List[str] = Field(default_factory=list)
    policy_applied: PolicyEnvironment
