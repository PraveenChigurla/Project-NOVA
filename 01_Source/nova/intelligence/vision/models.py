"""
Vision Framework Models.
Defines strict, immutable schemas for visual data aggregation.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class BoundingBox(BaseModel):
    """Geometric coordinates of a detected region on the screen."""
    left: int = Field(..., description="X coordinate of the top-left corner")
    top: int = Field(..., description="Y coordinate of the top-left corner")
    width: int = Field(..., description="Width of the bounding box")
    height: int = Field(..., description="Height of the bounding box")

    @property
    def center_x(self) -> int:
        return self.left + (self.width // 2)

    @property
    def center_y(self) -> int:
        return self.top + (self.height // 2)
        
    class Config:
        frozen = True

class DetectedRegion(BaseModel):
    """Base class for any spatial data detected in an image."""
    box: BoundingBox = Field(..., description="The spatial bounds of the detection")
    confidence: float = Field(..., description="Provider confidence score (0.0 to 1.0)")
    source_provider: str = Field(..., description="ID of the provider that generated this detection")

    class Config:
        frozen = True

class DetectedText(DetectedRegion):
    """Text extracted from an image (OCR)."""
    text: str = Field(..., description="The string extracted from the bounding box")
    language: str = Field(default="eng", description="Language of the detected text")
    block_index: int = Field(default=0, description="Structural block index")
    line_index: int = Field(default=0, description="Line index within the block")
    reading_order: int = Field(default=0, description="Overall reading order index")

class DetectedObject(DetectedRegion):
    """An object or UI element identified in an image."""
    label: str = Field(..., description="The class/label of the object (e.g., 'button', 'icon')")
    text: Optional[str] = Field(None, description="Semantic text associated with this object (e.g. 'Save' on a button)")
    attributes: Dict[str, Any] = Field(default_factory=dict, description="Optional metadata (e.g., color, state)")

class VisionMetadata(BaseModel):
    """Metadata about the source image."""
    image_path: str = Field(..., description="Path to the source image file")
    resolution: str = Field(default="", description="Resolution (e.g., '1920x1080')")
    timestamp: float = Field(..., description="Epoch timestamp of the capture")
    
    class Config:
        frozen = True

class VisionRequest(BaseModel):
    """The input payload sent to the Vision Engine."""
    image_path: str = Field(..., description="Path to the image to analyze")
    required_capabilities: List[str] = Field(default_factory=list, description="Capabilities to run (e.g., 'ocr', 'object_detection'). Empty means run all available.")
    
    class Config:
        frozen = True

class VisionResult(BaseModel):
    """The massive unified payload containing all aggregated detections."""
    metadata: VisionMetadata = Field(..., description="Metadata of the source image")
    text: List[DetectedText] = Field(default_factory=list, description="Aggregated OCR results")
    objects: List[DetectedObject] = Field(default_factory=list, description="Aggregated object detection results")
    errors: List[str] = Field(default_factory=list, description="Errors encountered by individual providers")
    
    class Config:
        frozen = True
