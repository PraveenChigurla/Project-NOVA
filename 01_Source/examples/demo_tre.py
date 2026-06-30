"""
Project NOVA - Target Resolution Engine Demonstration.
Proves that NOVA can reason spatially over a semantic World Model.
"""

import asyncio
import logging
import sys
import time

from nova.intelligence.vision.models import VisionResult, VisionMetadata, DetectedText, DetectedObject, BoundingBox
from nova.intelligence.resolution.engine import TargetResolutionEngine
from nova.intelligence.resolution.models import TargetQuery, SpatialRelation

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("nova.demo_tre")

def build_mock_world_model() -> VisionResult:
    """Simulates a complex screen with multiple identical buttons."""
    metadata = VisionMetadata(image_path="mock.png", timestamp=time.time())
    
    # Let's mock a login screen layout
    # [        Username        ]
    # [        Password        ]
    # [Login1] [Login2] [Login3]
    
    objects = [
        DetectedObject(
            source_provider="mock",
            confidence=0.99,
            box=BoundingBox(left=500, top=200, width=200, height=40),
            label="input",
            text="Username"
        ),
        DetectedObject(
            source_provider="mock",
            confidence=0.99,
            box=BoundingBox(left=500, top=300, width=200, height=40),
            label="input",
            text="Password"
        ),
        DetectedObject(
            source_provider="mock",
            confidence=0.95,
            box=BoundingBox(left=400, top=400, width=100, height=40),
            label="button",
            text="Login" # Incorrect login (Left)
        ),
        DetectedObject(
            source_provider="mock",
            confidence=0.97,
            box=BoundingBox(left=550, top=400, width=100, height=40),
            label="button",
            text="Login" # Correct login (Directly below Password)
        ),
        DetectedObject(
            source_provider="mock",
            confidence=0.94,
            box=BoundingBox(left=700, top=400, width=100, height=40),
            label="button",
            text="Login" # Incorrect login (Right)
        )
    ]
    
    return VisionResult(metadata=metadata, text=[], objects=objects, errors=[])

def main():
    logger.info("Initializing Target Resolution Engine...")
    tre = TargetResolutionEngine()
    
    world_model = build_mock_world_model()
    
    # Query 1: Find any "Password" field
    logger.info("\n>>> Scenario 1: Simple Semantic Query <<<")
    q1 = TargetQuery(target_text="Password", target_type="input")
    res1 = tre.resolve(world_model, q1)
    if res1:
        logger.info(f"Resolved! [{res1.box.center_x}, {res1.box.center_y}] - Reason: {res1.reason}")

    # Query 2: Spatial Reasoning
    logger.info("\n>>> Scenario 2: Spatial Reasoning ('Login' BELOW 'Password') <<<")
    # There are 3 Login buttons. The TRE must mathematically identify the correct one.
    q2 = TargetQuery(
        target_text="Login", 
        target_type="button",
        relation=SpatialRelation.BELOW,
        reference_text="Password",
        reference_type="input"
    )
    res2 = tre.resolve(world_model, q2)
    if res2:
        logger.info(f"Resolved! Target Center: [{res2.box.center_x}, {res2.box.center_y}]")
        logger.info(f"Reasoning: {res2.reason}")
        
    logger.info("\nTRE Demonstration Complete. NOVA can now think spatially.")

if __name__ == "__main__":
    main()
