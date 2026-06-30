"""
Unit tests for the Vision Framework.
"""

import pytest
import asyncio
from nova.intelligence.vision.engine import VisionEngine
from nova.intelligence.vision.registry import VisionRegistry
from nova.intelligence.vision.models import VisionRequest
from nova.providers.vision.mock_ocr_provider import MockVisionProvider

@pytest.mark.asyncio
async def test_vision_engine_aggregation():
    registry = VisionRegistry()
    registry.register(MockVisionProvider("test.ocr", ["ocr"]))
    registry.register(MockVisionProvider("test.obj", ["object_detection"]))
    
    engine = VisionEngine(registry)
    req = VisionRequest(image_path="/test", required_capabilities=[])
    
    result = await engine.analyze(req)
    
    # Verify aggregation
    assert len(result.text) == 2
    assert len(result.objects) == 2
    
    # Verify semantic target support
    assert result.objects[0].text == "Save"
    assert result.objects[0].label == "button"
    
    # Verify metadata fallback/passthrough
    assert result.metadata.image_path == "/test"
    assert result.metadata.resolution == "1920x1080"
