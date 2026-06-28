"""
Intent Registry.
Stores definitions of all intents NOVA understands.
"""

from typing import Dict, List, Optional
import logging

from nova.intelligence.intents.models import Intent

logger = logging.getLogger(__name__)

class IntentRegistry:
    """Manages the catalog of known intents."""
    
    def __init__(self):
        self._intents: Dict[str, Intent] = {}
        
    def register(self, intent: Intent) -> None:
        """Registers a new intent."""
        if intent.name in self._intents:
            logger.warning(f"Intent '{intent.name}' is already registered. Overwriting.")
        self._intents[intent.name] = intent
        logger.debug(f"Registered intent: {intent.name}")
        
    def get(self, intent_name: str) -> Optional[Intent]:
        """Retrieves an intent by name."""
        return self._intents.get(intent_name)
        
    def get_all(self) -> List[Intent]:
        """Returns all registered intents."""
        return list(self._intents.values())
