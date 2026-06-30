"""
CLI Input Adapter.
Reads input from standard in.
"""
import uuid
from nova.intelligence.input.adapters.base import BaseInputAdapter
from nova.intelligence.input.models import NormalizedInput

class CLIAdapter(BaseInputAdapter):
    """Adapter for Terminal/CLI inputs."""
    
    def __init__(self, session_id: str = None):
        self.session_id = session_id or str(uuid.uuid4())
        
    def listen(self) -> NormalizedInput:
        """Blocks until the user types something in the terminal."""
        text = input("NOVA> ")
        return NormalizedInput(
            text=text,
            source="cli",
            session_id=self.session_id,
            confidence=1.0 # Text is always 100% confident
        )
