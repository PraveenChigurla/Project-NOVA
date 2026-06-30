"""
Base Input Adapter.
The abstract class that all input sources (Voice, CLI, REST) must implement.
"""
from abc import ABC, abstractmethod
from nova.intelligence.input.models import NormalizedInput

class BaseInputAdapter(ABC):
    """Translates a specific input medium into a NormalizedInput."""
    
    @abstractmethod
    def listen(self) -> NormalizedInput:
        """
        Blocks or triggers to capture input, returning a NormalizedInput.
        In an async framework, this might be an async generator.
        """
        pass
