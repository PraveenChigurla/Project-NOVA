"""
Project NOVA - OCR Provider Demonstration.
Captures the active screen and extracts semantic text.
"""
import asyncio
import logging
import sys
import os

from nova.core.config import NovaConfig
from nova.core.kernel import NovaKernel
from nova.intelligence.planning.models import ExecutionPlan, PlanStep, ExecutionStrategy
from nova.security.permissions.models import PermissionScope
from nova.intelligence.vision.models import VisionRequest
from nova.providers.vision.ocr.provider import OCRProvider

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("nova.demo_ocr")

async def main():
    logger.info("Initializing NOVA Kernel for OCR Demo...")
    config = NovaConfig()
    kernel = NovaKernel(config)
    await kernel.boot()
    
    # Register OCR Provider into Vision Framework
    ocr_plugin = OCRProvider()
    
    # Grant permission for screen capture
    logger.info("Granting Permission: OS_WINDOW_CAPTURE")
    await kernel.permission_manager.grant("com.nova.vision.screen", PermissionScope.OS_WINDOW_CAPTURE)
    
    # Step 1: Capture the screen using the Execution Engine pipeline
    plan = ExecutionPlan(
        intent="Capture Active Monitor",
        strategy=ExecutionStrategy.SEQUENTIAL,
        steps=[
            PlanStep(
                step_id="capture",
                capability_id="com.nova.vision.screen",
                action="capture_active_monitor",
                parameters={},
                dependencies=[]
            )
        ]
    )
    
    logger.info("Capturing Screen...")
    result = await kernel.execution_engine.execute_plan(plan)
    
    if not result.success:
        logger.error("Failed to capture screen.")
        return
        
    image_path = result.step_results[0].data.get("image_path")
    logger.info(f"Screen captured successfully: {image_path}")
    
    # Step 2: Pass image to OCR Provider natively
    logger.info("Running OCR Pipeline...")
    req = VisionRequest(image_path=image_path, required_capabilities=["ocr"])
    vision_result = await ocr_plugin.process(req)
    
    logger.info("\n=========================================")
    logger.info("          EXTRACTED SEMANTIC TEXT        ")
    logger.info("=========================================")
    
    for text_obj in vision_result.text:
        # Reconstruct the line using semantic data
        print(f"[{text_obj.box.left:>4}, {text_obj.box.top:>4}] {text_obj.text}")
        
    logger.info("\nPipeline execution complete.")
    await kernel.shutdown()
    
    # Cleanup capture
    if os.path.exists(image_path):
        os.remove(image_path)

if __name__ == "__main__":
    if os.name != 'nt':
        logger.error("This demonstration runs on Windows.")
        sys.exit(1)
    asyncio.run(main())
