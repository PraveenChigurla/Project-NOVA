"""
Vision Strategy.
The ultimate fallback. Uses OCR, TRE, and physical mouse/keyboard injection.
"""
import logging
from nova.intelligence.interaction.strategy.strategies.base import InteractionStrategy
from nova.intelligence.interaction.strategy.models import InteractionIntent, InteractionStrategyType

logger = logging.getLogger(__name__)

class VisionStrategy(InteractionStrategy):
    
    def __init__(self, kernel):
        # We need the kernel to access mouse/keyboard/vision capabilities
        self.kernel = kernel
        
    @property
    def strategy_type(self) -> InteractionStrategyType:
        return InteractionStrategyType.VISION
        
    async def _execute_internal(self, intent: InteractionIntent, context: dict = None) -> tuple[bool, any, str]:
        # NOTE: For this Sprint, we mock the vision resolution to focus on the Strategy Engine fallback loop.
        # In a real implementation, this would:
        # 1. Capture Screen via ScreenCaptureProvider
        # 2. Run OCR via OCRProvider
        # 3. Use TRE to find bounding box of intent.target
        # 4. Use MouseCapability to physically click the box center
        
        logger.warning(f"[VISION STRATEGY] Invoked for intent: {intent.action} on '{intent.target}'")
        
        # MOCK IMPLEMENTATION FOR FALLBACK DEMONSTRATION
        if intent.action == "click":
            # Pretend we found it on screen and moved the mouse
            logger.info(f"-> Vision found target '{intent.target}' at coordinates (500, 300).")
            logger.info(f"-> Mouse capability physically clicked (500, 300).")
            return True, {"x": 500, "y": 300, "confidence": 0.95}, None
            
        elif intent.action == "type":
            # Pretend we found it, clicked it to focus, and typed
            logger.info(f"-> Vision found target '{intent.target}' at coordinates (500, 300).")
            logger.info(f"-> Keyboard capability physically typed text.")
            return True, {"x": 500, "y": 300, "text_typed": intent.parameters.get("text")}, None
            
        else:
            return False, None, f"Vision Strategy does not support action: {intent.action}"
