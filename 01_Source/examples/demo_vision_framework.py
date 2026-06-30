"""
Project NOVA - Vision Framework Demonstration.
Proves the Vision Engine dispatches to multiple plugins and aggregates semantic targets.
"""

import asyncio
import logging
import sys

from nova.intelligence.vision.registry import VisionRegistry
from nova.intelligence.vision.engine import VisionEngine
from nova.intelligence.vision.models import VisionRequest
from nova.providers.vision.mock_ocr_provider import MockVisionProvider

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("nova.demo_vision")

async def main():
    logger.info("Initializing Vision Registry...")
    registry = VisionRegistry()
    
    # Register two separate plugins to prove aggregation
    ocr_plugin = MockVisionProvider("com.nova.vision.mock.ocr", ["ocr"])
    obj_plugin = MockVisionProvider("com.nova.vision.mock.yolo", ["object_detection"])
    
    registry.register(ocr_plugin)
    registry.register(obj_plugin)
    
    logger.info("Initializing Vision Engine...")
    engine = VisionEngine(registry)
    
    req = VisionRequest(
        image_path="/fake/path/screen.png",
        required_capabilities=[] # Run all
    )
    
    logger.info("\n>>> Executing Semantic Vision Analysis <<<")
    result = await engine.analyze(req)
    
    logger.info(f"\n--- Vision Result ---")
    logger.info(f"Metadata: {result.metadata.image_path} at {result.metadata.resolution}")
    
    logger.info(f"\n[Detected Text Regions: {len(result.text)}]")
    for t in result.text:
        logger.info(f"  - '{t.text}' (Conf: {t.confidence}) from {t.source_provider} at {t.box}")
        
    logger.info(f"\n[Detected Semantic Objects: {len(result.objects)}]")
    for o in result.objects:
        # Highlighting the new Semantic Labeling capability requested by user!
        semantic_label = f"[{o.label}] '{o.text}'" if o.text else f"[{o.label}]"
        logger.info(f"  - {semantic_label} (Conf: {o.confidence}) at {o.box}")
        
    if result.errors:
        logger.error(f"Errors: {result.errors}")

if __name__ == "__main__":
    asyncio.run(main())
