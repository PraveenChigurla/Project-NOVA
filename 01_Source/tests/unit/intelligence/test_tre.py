"""
Tests for Target Resolution Engine.
"""
import pytest
import time

from nova.intelligence.resolution.engine import TargetResolutionEngine
from nova.intelligence.resolution.models import TargetQuery, SpatialRelation
from nova.intelligence.vision.models import VisionResult, VisionMetadata, DetectedObject, BoundingBox

def test_tre_spatial_reasoning_below():
    tre = TargetResolutionEngine()
    
    # Anchor
    ref = DetectedObject(source_provider="mock", confidence=1.0, box=BoundingBox(left=100, top=100, width=50, height=50), label="input", text="Ref")
    
    # Candidates
    c1 = DetectedObject(source_provider="mock", confidence=1.0, box=BoundingBox(left=100, top=50, width=50, height=50), label="button", text="Target") # Above
    c2 = DetectedObject(source_provider="mock", confidence=1.0, box=BoundingBox(left=100, top=200, width=50, height=50), label="button", text="Target") # Below
    
    wm = VisionResult(
        metadata=VisionMetadata(image_path="test", timestamp=time.time()),
        text=[],
        objects=[ref, c1, c2],
        errors=[]
    )
    
    q = TargetQuery(target_text="Target", relation=SpatialRelation.BELOW, reference_text="Ref")
    res = tre.resolve(wm, q)
    
    assert res is not None
    assert res.box.top == 200 # Should pick c2

def test_tre_spatial_reasoning_nearest():
    tre = TargetResolutionEngine()
    
    ref = DetectedObject(source_provider="mock", confidence=1.0, box=BoundingBox(left=100, top=100, width=10, height=10), label="input", text="Ref")
    
    # Candidates
    c1 = DetectedObject(source_provider="mock", confidence=1.0, box=BoundingBox(left=100, top=120, width=10, height=10), label="button", text="Target") # Distance 20
    c2 = DetectedObject(source_provider="mock", confidence=1.0, box=BoundingBox(left=100, top=200, width=10, height=10), label="button", text="Target") # Distance 100
    
    wm = VisionResult(
        metadata=VisionMetadata(image_path="test", timestamp=time.time()),
        text=[],
        objects=[ref, c1, c2],
        errors=[]
    )
    
    q = TargetQuery(target_text="Target", relation=SpatialRelation.NEAREST, reference_text="Ref")
    res = tre.resolve(wm, q)
    
    assert res is not None
    assert res.box.top == 120 # Should pick c1
