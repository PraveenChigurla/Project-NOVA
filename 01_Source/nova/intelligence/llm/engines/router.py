"""
Model Router.
Selects the appropriate LLM provider based on the task.
"""
from typing import Dict
from nova.intelligence.llm.interfaces import LLMProvider

class ModelRouter:
    """Routes requests to the optimal LLM provider."""
    
    def __init__(self, default_provider: LLMProvider):
        self._providers: Dict[str, LLMProvider] = {"default": default_provider}
        self._default = default_provider
        
    def register_provider(self, name: str, provider: LLMProvider):
        self._providers[name] = provider
        
    def get_provider(self, capability: str = "default") -> LLMProvider:
        """Returns the requested provider, or the default if not found."""
        return self._providers.get(capability, self._default)
