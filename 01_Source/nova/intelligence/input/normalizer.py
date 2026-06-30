"""
Input Normalizer.
Validates and sanitizes NormalizedInputs before they reach the Conversation Manager.
"""
import logging
from nova.intelligence.input.models import NormalizedInput

logger = logging.getLogger(__name__)

class InputNormalizer:
    """Ensures input conforms to NOVA's standards (removes noise, low confidence, etc)."""
    
    def normalize(self, input_obj: NormalizedInput) -> NormalizedInput:
        logger.debug(f"InputNormalizer processing input from source: {input_obj.source}")
        
        # 1. Strip whitespace
        clean_text = input_obj.text.strip()
        
        # 2. Handle low confidence (e.g., garbled voice)
        if input_obj.confidence < 0.4:
            logger.warning(f"Input confidence ({input_obj.confidence}) is too low. Nullifying.")
            clean_text = ""
            
        # 3. Apply standard formatting
        if clean_text:
            # Capitalize first letter if not already
            clean_text = clean_text[0].upper() + clean_text[1:]
            
        input_obj.text = clean_text
        return input_obj
