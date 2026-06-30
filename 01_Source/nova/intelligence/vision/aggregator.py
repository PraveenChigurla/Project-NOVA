"""
Vision Aggregator.
Merges multiple partial VisionResults into a single coherent output.
"""
import logging
from typing import List
from nova.intelligence.vision.models import VisionResult, VisionMetadata

logger = logging.getLogger(__name__)

class VisionAggregator:
    """Aggregates an array of independent VisionResults."""
    
    @staticmethod
    def aggregate(base_metadata: VisionMetadata, results: List[VisionResult]) -> VisionResult:
        """
        Merges text, objects, and errors from all plugins into one payload.
        """
        all_text = []
        all_objects = []
        all_errors = []
        
        for res in results:
            all_text.extend(res.text)
            all_objects.extend(res.objects)
            all_errors.extend(res.errors)
            
        logger.debug(f"Aggregated {len(all_text)} text regions and {len(all_objects)} objects from {len(results)} plugins.")
        
        return VisionResult(
            metadata=base_metadata,
            text=all_text,
            objects=all_objects,
            errors=all_errors
        )
