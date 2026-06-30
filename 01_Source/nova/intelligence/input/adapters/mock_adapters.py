"""
Mock Input Adapters.
Simulates Voice and REST inputs for Sprint 23 validation.
"""
import uuid
from typing import Optional
from nova.intelligence.input.adapters.base import BaseInputAdapter
from nova.intelligence.input.models import NormalizedInput

class MockVoiceAdapter(BaseInputAdapter):
    """Simulates receiving a transcribed audio stream."""
    
    def __init__(self, simulated_text: str, session_id: str = None):
        self.simulated_text = simulated_text
        self.session_id = session_id or str(uuid.uuid4())
        self._consumed = False
        
    def listen(self) -> Optional[NormalizedInput]:
        if self._consumed:
            return None
        self._consumed = True
        return NormalizedInput(
            text=self.simulated_text,
            source="voice",
            session_id=self.session_id,
            confidence=0.85 # Voice is less confident
        )


class MockRESTAdapter(BaseInputAdapter):
    """Simulates receiving a JSON payload via an API endpoint."""
    
    def __init__(self, simulated_payload: dict, session_id: str = None):
        self.simulated_payload = simulated_payload
        self.session_id = session_id or str(uuid.uuid4())
        self._consumed = False
        
    def listen(self) -> Optional[NormalizedInput]:
        if self._consumed:
            return None
        self._consumed = True
        return NormalizedInput(
            text=self.simulated_payload.get("text", ""),
            source="rest",
            session_id=self.session_id,
            confidence=1.0,
            metadata={"origin_ip": self.simulated_payload.get("ip", "127.0.0.1")}
        )
