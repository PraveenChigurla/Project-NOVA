"""
Input Framework Models.
Defines the universal representations of input regardless of the source.
"""
import time
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class NormalizedInput(BaseModel):
    """The canonical representation of user input."""
    text: str
    source: str = Field(..., description="The adapter that generated this input (e.g., 'voice', 'cli', 'rest')")
    session_id: str
    timestamp: float = Field(default_factory=time.time)
    confidence: float = Field(default=1.0, description="Confidence of the transcription or extraction")
    metadata: Dict[str, Any] = Field(default_factory=dict)

class InputSession(BaseModel):
    """Tracks the ongoing conversation state."""
    session_id: str
    active: bool = True
    context_keys: Dict[str, Any] = Field(default_factory=dict)
    # The ConversationManager will use this to track pronouns and interruptions.
