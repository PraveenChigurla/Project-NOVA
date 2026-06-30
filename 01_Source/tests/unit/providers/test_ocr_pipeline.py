"""
Tests for OCR Pipeline components.
"""
import pytest
import numpy as np

from nova.providers.vision.ocr.models import OCRConfiguration, OCRMode
from nova.providers.vision.ocr.postprocessor import OCRPostprocessor

def test_ocr_postprocessor_filters_confidence():
    config = OCRConfiguration(confidence_threshold=0.8)
    
    raw = [
        {"left": 10, "top": 10, "width": 50, "height": 15, "confidence": 0.9, "text": "HighConf"},
        {"left": 70, "top": 10, "width": 50, "height": 15, "confidence": 0.5, "text": "LowConf"},
        {"left": 130, "top": 10, "width": 50, "height": 15, "confidence": 0.95, "text": "  "} # Empty text
    ]
    
    results = OCRPostprocessor.process(raw, config, "test")
    
    assert len(results) == 1
    assert results[0].text == "HighConf"
    
def test_ocr_postprocessor_scales_bounds_back():
    config = OCRConfiguration(scale_factor=2.0, enable_preprocessing=True)
    
    raw = [
        {"left": 100, "top": 100, "width": 50, "height": 50, "confidence": 0.9, "text": "Test"}
    ]
    
    results = OCRPostprocessor.process(raw, config, "test")
    
    # Coordinates should be divided by 2.0
    assert results[0].box.left == 50
    assert results[0].box.top == 50
    assert results[0].box.width == 25
    assert results[0].box.height == 25
