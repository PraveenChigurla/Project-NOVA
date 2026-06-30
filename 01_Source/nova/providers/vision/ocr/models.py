"""
OCR Provider Models.
"""
from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class OCRMode(str, Enum):
    FAST = "fast"
    ACCURATE = "accurate"
    REGION = "region"
    INCREMENTAL = "incremental"
    STREAMING = "streaming"

class OCRConfiguration(BaseModel):
    """Configuration for the OCR pipeline."""
    mode: OCRMode = Field(default=OCRMode.ACCURATE)
    enable_preprocessing: bool = Field(default=True)
    scale_factor: float = Field(default=2.0, description="Image scaling factor for accuracy")
    enable_denoise: bool = Field(default=True)
    enable_contrast: bool = Field(default=True)
    confidence_threshold: float = Field(default=0.6, description="Minimum confidence to keep a word")
    merge_adjacent: bool = Field(default=True, description="Merge words into semantic chunks/lines")

class OCRMetrics(BaseModel):
    """Timing and performance metrics for the OCR pipeline."""
    preprocessing_ms: float = 0.0
    inference_ms: float = 0.0
    postprocessing_ms: float = 0.0
    total_ms: float = 0.0

class OCRStatistics(BaseModel):
    """Statistics about the extracted text."""
    total_regions: int = 0
    total_words: int = 0
    average_confidence: float = 0.0
    metrics: OCRMetrics = Field(default_factory=OCRMetrics)
