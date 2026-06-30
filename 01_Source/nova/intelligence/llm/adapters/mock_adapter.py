"""
Mock LLM Adapter.
Simulates an LLM returning a structured GoalContract JSON for Sprint 22 validation.
"""
import logging
from typing import Dict, Any
from nova.intelligence.llm.interfaces import LLMProvider
from nova.intelligence.llm.models import ContextPayload

logger = logging.getLogger(__name__)

class MockLLMAdapter(LLMProvider):
    """A dummy provider that returns hardcoded responses based on simple heuristics."""
    
    def generate_contract(self, payload: ContextPayload) -> Dict[str, Any]:
        logger.info("MockLLMAdapter received prompt. Simulating inference...")
        
        intent_lower = payload.intent.lower()
        
        if "prepare" in intent_lower and "workday" in intent_lower:
            # Simulate a successful LLM extraction
            return {
                "goal_id": "prepare_workspace",
                "confidence": 0.98,
                "parameters": {"mode": "default"},
                "requires_confirmation": False,
                "reasoning_summary": "User wants to initialize their standard working environment.",
                "safety_flags": []
            }
        
        # Fallback for unknown intents
        return {
            "goal_id": "unknown_goal",
            "confidence": 0.1,
            "parameters": {},
            "requires_confirmation": True,
            "reasoning_summary": "Intent could not be mapped to a known goal.",
            "safety_flags": ["ambiguous_intent"]
        }
