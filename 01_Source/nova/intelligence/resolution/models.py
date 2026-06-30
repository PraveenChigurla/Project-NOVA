"""
Target Resolution Models.
Defines schemas for requesting and resolving semantic targets in the World Model.
"""
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field
from nova.intelligence.vision.models import BoundingBox

class SpatialRelation(str, Enum):
    """Supported geometric relationships."""
    LEFT_OF = "left_of"
    RIGHT_OF = "right_of"
    ABOVE = "above"
    BELOW = "below"
    NEAREST = "nearest"
    INSIDE = "inside"
    CONTAINS = "contains"

class TargetQuery(BaseModel):
    """
    A strict request to find a specific semantic target within a VisionResult.
    Example: TargetQuery(target_text="Login", relation=SpatialRelation.BELOW, reference_text="Password")
    """
    target_text: str = Field(..., description="The semantic text or label of the target being searched for.")
    target_type: Optional[str] = Field(None, description="Optional filter (e.g., 'button', 'text', 'icon').")
    
    relation: Optional[SpatialRelation] = Field(None, description="Spatial relation to the reference.")
    reference_text: Optional[str] = Field(None, description="The semantic text of the reference anchor.")
    reference_type: Optional[str] = Field(None, description="Optional filter for the reference anchor.")

class ResolvedTarget(BaseModel):
    """The final, actionable object returned by the TRE to the Execution Engine."""
    box: BoundingBox = Field(..., description="The exact coordinates of the resolved target.")
    semantic_label: str = Field(..., description="The label or text of the resolved target.")
    confidence: float = Field(..., description="The engine's confidence that this is the correct target (0.0 - 1.0).")
    reason: str = Field(..., description="Mathematical explanation of why this target was chosen.")
