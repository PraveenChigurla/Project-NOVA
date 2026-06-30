"""
Goal Contract Validator.
Ensures the raw LLM output is a valid, safe GoalContract.
"""
import logging
from typing import Dict, Any
from nova.intelligence.llm.models import GoalContract

logger = logging.getLogger(__name__)

class GoalContractValidator:
    """Validates and instantiates the GoalContract."""
    
    def validate(self, raw_response: Dict[str, Any]) -> GoalContract:
        try:
            # Pydantic handles type coercion and required fields
            contract = GoalContract(**raw_response)
            
            # Custom safety rules
            if contract.confidence < 0.5:
                logger.warning("LLM Confidence is low. Forcing user confirmation.")
                contract.requires_confirmation = True
                
            if "destructive" in contract.safety_flags:
                logger.warning("Destructive safety flag detected. Forcing user confirmation.")
                contract.requires_confirmation = True
                
            return contract
            
        except Exception as e:
            logger.error(f"Failed to validate GoalContract from LLM output: {e}")
            # Return a safe fallback contract
            return GoalContract(
                goal_id="validation_failed",
                confidence=0.0,
                reasoning_summary=f"Validation failed: {e}",
                requires_confirmation=True,
                safety_flags=["validation_error"]
            )
