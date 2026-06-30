"""
LLM Provider Interfaces.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
from nova.intelligence.llm.models import ContextPayload

class LLMProvider(ABC):
    """Abstract base class for all Language Model providers (OpenAI, Gemini, Local, etc.)."""
    
    @abstractmethod
    def generate_contract(self, payload: ContextPayload) -> Dict[str, Any]:
        """
        Takes the ContextPayload and returns a raw dictionary representing the GoalContract.
        The caller is responsible for validating this dictionary against the GoalContract Pydantic model.
        """
        pass
