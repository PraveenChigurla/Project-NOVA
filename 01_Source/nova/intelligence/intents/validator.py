"""
Intent Validator.
Ensures that an extracted intent contains all required entities.
"""

from nova.intelligence.intents.models import Intent, IntentResult
import logging

logger = logging.getLogger(__name__)

class IntentValidator:
    """Validates the completeness of an extracted intent result."""
    
    @staticmethod
    def validate(result: IntentResult, intent_def: Intent) -> IntentResult:
        """
        Checks if the result has all required entities.
        If missing, lowers confidence and marks is_valid=False.
        """
        is_valid = True
        confidence = result.confidence
        
        missing_entities = []
        for req in intent_def.required_entities:
            if req not in result.entities:
                missing_entities.append(req)
                is_valid = False
                
        if missing_entities:
            logger.debug(f"Intent '{result.intent_name}' missing required entities: {missing_entities}")
            confidence *= 0.5 # drastically reduce confidence if missing parameters
            
        # Return a new modified copy (since it's frozen)
        return IntentResult(
            intent_name=result.intent_name,
            entities=result.entities,
            confidence=confidence,
            original_input=result.original_input,
            is_valid=is_valid
        )
