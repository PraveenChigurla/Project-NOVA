"""
Vision Engine.
Master orchestrator for the Perception tier. 
Coordinates resolution and aggregation of visual providers.
"""
import logging
import asyncio
from typing import List

from nova.intelligence.vision.registry import VisionRegistry
from nova.intelligence.vision.resolver import VisionResolver
from nova.intelligence.vision.aggregator import VisionAggregator
from nova.intelligence.vision.models import VisionRequest, VisionResult, VisionMetadata

logger = logging.getLogger(__name__)

class VisionEngine:
    """Orchestrates image analysis across multiple concurrent providers."""
    
    def __init__(self, registry: VisionRegistry):
        self.registry = registry
        self.resolver = VisionResolver(registry)
        self.aggregator = VisionAggregator()
        
    async def analyze(self, request: VisionRequest) -> VisionResult:
        """
        Dispatches the image to all resolved plugins, waits for them,
        and aggregates their bounding boxes into a unified semantic map.
        """
        plugins = self.resolver.resolve(request)
        
        if not plugins:
            logger.warning(f"No vision plugins resolved for request capabilities: {request.required_capabilities}")
            import time
            base_metadata = VisionMetadata(
                image_path=request.image_path,
                timestamp=time.time()
            )
            return VisionResult(metadata=base_metadata, errors=["No providers resolved"])
            
        logger.info(f"Dispatching vision request to {len(plugins)} plugins concurrently...")
        
        # Execute all plugins concurrently
        tasks = [plugin.process(request) for plugin in plugins]
        results: List[VisionResult] = await asyncio.gather(*tasks, return_exceptions=True)
        
        valid_results = []
        errors = []
        
        for i, res in enumerate(results):
            if isinstance(res, Exception):
                logger.error(f"Plugin {plugins[i].plugin_id} failed: {res}")
                errors.append(f"{plugins[i].plugin_id}: {str(res)}")
            else:
                valid_results.append(res)
                
        # Generate base metadata from the first valid result, or fallback
        import time
        if valid_results:
            base_metadata = valid_results[0].metadata
        else:
            base_metadata = VisionMetadata(
                image_path=request.image_path,
                timestamp=time.time()
            )
            
        aggregated_result = self.aggregator.aggregate(base_metadata, valid_results)
        
        # Merge execution errors if any
        if errors:
            all_errors = list(aggregated_result.errors) + errors
            aggregated_result = VisionResult(
                metadata=aggregated_result.metadata,
                text=aggregated_result.text,
                objects=aggregated_result.objects,
                errors=all_errors
            )
            
        return aggregated_result
