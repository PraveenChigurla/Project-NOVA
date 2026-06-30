"""
Goal Engine.
Translates raw natural language intents into normalized Goals.
"""
import logging
from typing import Optional
from nova.intelligence.cognition.models import Goal
from nova.intelligence.llm.models import GoalContract

logger = logging.getLogger(__name__)

class GoalEngine:
    """Normalizes GoalContracts from the LLM into canonical Goal objects for the Planner."""
    
    def normalize(self, contract: GoalContract, raw_intent: str) -> Goal:
        logger.debug(f"GoalEngine normalizing contract: '{contract.goal_id}'")
        
        # In a real implementation, this engine might map the LLM's goal_id to 
        # a strictly known subset of capability IDs, or fetch goal metadata.
        # For now, it simply bridges the LLM Contract into the Cognitive Goal.
        
        goal = Goal(
            id=contract.goal_id,
            raw_intent=raw_intent,
            parameters=contract.parameters
        )
        
        logger.info(f"Resolved Goal ID: {goal.id}")
        return goal
