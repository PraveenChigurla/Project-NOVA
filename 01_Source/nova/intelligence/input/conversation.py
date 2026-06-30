"""
Conversation Manager.
Maintains input sessions and context across multiple interactions.
"""
import logging
from typing import Dict, List
from nova.intelligence.input.models import NormalizedInput, InputSession

logger = logging.getLogger(__name__)

class ConversationManager:
    """Manages conversational context."""
    
    def __init__(self):
        self.sessions: Dict[str, InputSession] = {}
        self.history: Dict[str, List[NormalizedInput]] = {}
        
    def get_or_create_session(self, session_id: str) -> InputSession:
        if session_id not in self.sessions:
            logger.info(f"Creating new InputSession: {session_id}")
            self.sessions[session_id] = InputSession(session_id=session_id)
            self.history[session_id] = []
        return self.sessions[session_id]
        
    def process(self, input_obj: NormalizedInput) -> NormalizedInput:
        """Records the input into history and returns it for downstream processing."""
        session = self.get_or_create_session(input_obj.session_id)
        
        # Add to history
        self.history[session.session_id].append(input_obj)
        
        logger.debug(f"ConversationManager processed input. Session '{session.session_id}' now has {len(self.history[session.session_id])} interactions.")
        
        # In the future, this is where Pronoun Resolution ("Open it") would occur by looking at history.
        return input_obj
