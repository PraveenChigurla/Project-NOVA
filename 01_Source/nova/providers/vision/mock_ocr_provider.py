"""
Mock Vision Provider.
Returns synthetic semantic targets (DetectedText and DetectedObject) for testing aggregation.
"""
import time
from typing import List

from nova.intelligence.vision.registry import IVisionPlugin
from nova.intelligence.vision.models import (
    VisionRequest, VisionResult, VisionMetadata, 
    DetectedText, DetectedObject, BoundingBox
)

class MockVisionProvider(IVisionPlugin):
    """A mock provider that pretends to detect semantic text and UI objects."""
    
    def __init__(self, plugin_id: str, capabilities: List[str]):
        self._plugin_id = plugin_id
        self._capabilities = capabilities
        
    @property
    def plugin_id(self) -> str:
        return self._plugin_id
        
    @property
    def capabilities(self) -> List[str]:
        return self._capabilities
        
    async def process(self, request: VisionRequest) -> VisionResult:
        """Returns synthetic data based on its ID."""
        
        metadata = VisionMetadata(
            image_path=request.image_path,
            resolution="1920x1080",
            timestamp=time.time()
        )
        
        text = []
        objects = []
        
        # Simulate OCR detection
        if "ocr" in self._capabilities:
            text.append(DetectedText(
                source_provider=self.plugin_id,
                confidence=0.98,
                box=BoundingBox(left=100, top=100, width=50, height=20),
                text="Ravi"
            ))
            text.append(DetectedText(
                source_provider=self.plugin_id,
                confidence=0.95,
                box=BoundingBox(left=200, top=300, width=150, height=30),
                text="Project NOVA"
            ))
            
        # Simulate Object detection
        if "object_detection" in self._capabilities:
            objects.append(DetectedObject(
                source_provider=self.plugin_id,
                confidence=0.96,
                box=BoundingBox(left=800, top=600, width=120, height=40),
                label="button",
                text="Save", # Semantic linking!
                attributes={"color": "blue", "state": "active"}
            ))
            objects.append(DetectedObject(
                source_provider=self.plugin_id,
                confidence=0.88,
                box=BoundingBox(left=10, top=10, width=32, height=32),
                label="icon",
                text="Settings",
                attributes={}
            ))
            
        return VisionResult(
            metadata=metadata,
            text=text,
            objects=objects,
            errors=[]
        )
