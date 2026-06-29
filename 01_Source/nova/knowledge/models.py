"""
Knowledge Exchange Network Models.
"""
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from nova.security.trust.models import PackageManifest

class KnowledgeManifest(PackageManifest):
    """Extends the standard package manifest for Knowledge artifacts."""
    evidence_score: float = 1.0
    applicable_versions: List[str] = Field(default_factory=list)

class KnowledgeData(BaseModel):
    """The actual payload of the learning."""
    category: str
    target: str
    payload: Dict[str, Any]
    
class KnowledgePackage(BaseModel):
    """The in-memory representation of a .kpkg file."""
    manifest: KnowledgeManifest
    data: KnowledgeData
    evidence_summary: str
