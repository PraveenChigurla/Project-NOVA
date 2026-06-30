"""
OCR Postprocessor.
Cleans up, merges, and semantically chunks raw OCR bounding boxes.
"""
import logging
from typing import List, Dict

from nova.intelligence.vision.models import DetectedText, BoundingBox
from nova.providers.vision.ocr.models import OCRConfiguration

logger = logging.getLogger(__name__)

class OCRPostprocessor:
    """Refines raw OCR engine outputs into clean semantic objects."""
    
    @staticmethod
    def process(
        raw_detections: List[Dict], 
        config: OCRConfiguration, 
        provider_id: str
    ) -> List[DetectedText]:
        """
        Takes raw dictionaries from pytesseract/paddleocr and converts them to 
        normalized DetectedText objects, applying filters and merging algorithms.
        """
        filtered = []
        
        # 1. Filter by Confidence & Clean Whitespace
        for det in raw_detections:
            conf = det.get("confidence", 0.0)
            text = det.get("text", "").strip()
            
            if conf < config.confidence_threshold:
                continue
            if not text:
                continue
                
            filtered.append(det)
            
        logger.debug(f"Filtered {len(raw_detections)} raw boxes down to {len(filtered)} confident boxes.")
        
        # 2. Merge Adjacent (Line merging) - Simplified for this sprint
        # In a full production implementation, we would sort by Y, then X, 
        # and merge bounding boxes that intersect horizontally within a threshold.
        # For now, we will just convert them to DetectedText objects.
        
        results = []
        for det in filtered:
            # Revert the scale factor applied during preprocessing!
            # If the image was upscaled 2x, the bounding box coordinates are 2x larger.
            # We must map them back to the original screen coordinates.
            sf = config.scale_factor if config.enable_preprocessing else 1.0
            
            left = int(det["left"] / sf)
            top = int(det["top"] / sf)
            width = int(det["width"] / sf)
            height = int(det["height"] / sf)
            
            results.append(
                DetectedText(
                    source_provider=provider_id,
                    confidence=det["confidence"],
                    box=BoundingBox(left=left, top=top, width=width, height=height),
                    text=det["text"],
                    language=det.get("language", "eng"),
                    block_index=det.get("block_index", 0),
                    line_index=det.get("line_index", 0),
                    reading_order=det.get("reading_order", 0)
                )
            )
            
        return results
