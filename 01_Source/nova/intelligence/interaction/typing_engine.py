"""
Typing Interaction Engine.
Calculates realistic human typing streams and cadences.
"""
import random
import logging
from typing import List, Tuple

from nova.intelligence.interaction.models import TypingProfile, InteractionConfig

logger = logging.getLogger(__name__)

class TypingEngine:
    """Generates mathematically human-like typing cadences."""
    
    def __init__(self, config: InteractionConfig = None):
        self.config = config or InteractionConfig()
        
    def generate_typing_stream(self, text: str, profile: TypingProfile = None) -> List[Tuple[str, float]]:
        """
        Generates a sequence of (character, delay_after_sec) tuples.
        """
        prof = profile or self.config.typing_profile
        logger.debug(f"Generating {prof.value} typing stream for {len(text)} characters.")
        
        if prof == TypingProfile.INSTANT:
            # Entire string, 0 delay
            return [(text, 0.0)]
            
        stream = []
        burst_count = 0
        
        for i, char in enumerate(text):
            delay = self._calculate_delay(char, prof, burst_count)
            stream.append((char, delay))
            
            if prof == TypingProfile.DEVELOPER:
                burst_count = (burst_count + 1) % random.randint(4, 10)
                if burst_count == 0:
                    # Occasional longer pause between bursts
                    delay += random.uniform(0.1, 0.3)
                    stream[-1] = (char, delay)
                    
        return stream

    def _calculate_delay(self, char: str, profile: TypingProfile, burst_count: int) -> float:
        """Calculates realistic delays based on the character type and profile."""
        if profile == TypingProfile.FAST:
            base_delay = random.uniform(0.01, 0.03)
        elif profile == TypingProfile.NATURAL:
            base_delay = random.uniform(0.04, 0.12)
        elif profile == TypingProfile.DEVELOPER:
            base_delay = random.uniform(0.02, 0.08)
        else: # ACCESSIBILITY
            base_delay = random.uniform(0.25, 0.5)
            
        # Add delay for capital letters or symbols (shift key simulation)
        if char.isupper() or char in "!@#$%^&*()_+{}|:\"<>?~":
            base_delay *= random.uniform(1.2, 1.5)
            
        # Spacebars are usually hit very quickly in succession
        if char == " ":
            base_delay *= random.uniform(0.7, 0.9)
            
        return base_delay
