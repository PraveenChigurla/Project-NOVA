"""
Intent Parsers.
Converts raw text into an IntentResult.
"""

from abc import ABC, abstractmethod
from typing import Optional
import re
import logging

from nova.intelligence.intents.models import IntentResult, Intent
from nova.intelligence.intents.registry import IntentRegistry
from nova.intelligence.intents.validator import IntentValidator

logger = logging.getLogger(__name__)

class IntentParser(ABC):
    """Abstract base class for all Intent Parsers (Rule-based, LLM-based, etc)."""
    
    def __init__(self, registry: IntentRegistry):
        self.registry = registry
        
    @abstractmethod
    async def parse(self, raw_input: str) -> IntentResult:
        """Parses the raw input and returns an IntentResult."""
        pass

class RuleIntentParser(IntentParser):
    """
    Phase 1 deterministic intent parser.
    Uses Regex and keyword matching to extract intents and entities.
    """
    
    async def parse(self, raw_input: str) -> IntentResult:
        logger.info(f"RuleIntentParser parsing input: '{raw_input}'")
        best_match: Optional[IntentResult] = None
        best_intent_def: Optional[Intent] = None
        
        # Iterate over all registered intents
        for intent in self.registry.get_all():
            for alias in intent.aliases:
                # Compile regex, ignoring case
                try:
                    pattern = re.compile(alias.pattern, re.IGNORECASE)
                    match = pattern.search(raw_input)
                    if match:
                        # Extract entities based on regex groups
                        entities = {}
                        for group_idx, entity_name in alias.entities_map.items():
                            try:
                                entities[entity_name] = match.group(group_idx)
                            except IndexError:
                                pass # Group not found in regex
                                
                        # We found a match, create a result
                        # For now, regex match is 1.0 confidence before validation
                        candidate = IntentResult(
                            intent_name=intent.name,
                            entities=entities,
                            confidence=1.0,
                            original_input=raw_input
                        )
                        
                        # Use first match (could expand to find best match if multiple exist)
                        best_match = candidate
                        best_intent_def = intent
                        break 
                except re.error as e:
                    logger.error(f"Invalid regex in alias for intent {intent.name}: {e}")
            
            if best_match:
                break
                
        if best_match and best_intent_def:
            # Validate the extracted result against the intent requirements
            validated_result = IntentValidator.validate(best_match, best_intent_def)
            logger.info(f"Parsed Intent: {validated_result.intent_name} with confidence {validated_result.confidence}")
            return validated_result
            
        # No match found
        logger.warning(f"Failed to parse any known intent from input: '{raw_input}'")
        return IntentResult(
            intent_name="unknown",
            entities={},
            confidence=0.0,
            original_input=raw_input,
            is_valid=False
        )
