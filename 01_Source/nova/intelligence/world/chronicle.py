"""
Event Chronicle.
Maintains an immutable, append-only log of significant lifecycle events.
"""
import time
from typing import List, Dict, Any
from pydantic import BaseModel, Field

class LifeEvent(BaseModel):
    """An immutable record of something that happened in NOVA."""
    timestamp: float = Field(default_factory=time.time)
    event_type: str = Field(..., description="e.g., 'GoalReceived', 'PlanGenerated', 'ExecutionStarted'")
    details: Dict[str, Any] = Field(default_factory=dict)

class EventChronicle:
    """The append-only log."""
    
    def __init__(self):
        self._events: List[LifeEvent] = []
        
    def record(self, event_type: str, details: Dict[str, Any] = None):
        """Appends a new event to the chronicle."""
        event = LifeEvent(event_type=event_type, details=details or {})
        self._events.append(event)
        
    def get_events(self) -> List[LifeEvent]:
        return list(self._events)
