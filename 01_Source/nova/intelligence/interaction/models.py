"""
Interaction Engine Models.
Defines parameters for human-like automation.
"""
from enum import Enum
from pydantic import BaseModel, Field

class MovementProfile(str, Enum):
    """Defines the cadence and speed of a mouse movement."""
    INSTANT = "instant"     # Teleports (Bot-like, 0ms)
    FAST = "fast"           # Linear glide, very fast (100ms)
    NATURAL = "natural"     # Bezier curve, acceleration/deceleration, human-like (300-600ms)
    PRECISE = "precise"     # Natural curve but slows down heavily near the target (600-1000ms)

class TypingProfile(str, Enum):
    """Defines the cadence and speed of typing."""
    INSTANT = "instant"           # Uses OS clipboard or 0ms native text injection
    FAST = "fast"                 # Minimal delay between keystrokes (20ms)
    NATURAL = "natural"           # Human delays with random variances (50-150ms)
    DEVELOPER = "developer"       # Bursts of very fast typing with short pauses
    ACCESSIBILITY = "accessibility" # Very slow typing (300ms+)

class InteractionConfig(BaseModel):
    """Configuration for an Interaction sequence."""
    mouse_profile: MovementProfile = Field(default=MovementProfile.NATURAL, description="Movement style.")
    typing_profile: TypingProfile = Field(default=TypingProfile.NATURAL, description="Typing cadence.")
    jitter: float = Field(default=0.1, description="Amount of random deviation in the Bezier control points (0.0 to 1.0).")
    hover_delay_ms: int = Field(default=200, description="Milliseconds to wait after moving before clicking.")
    click_delay_ms: int = Field(default=50, description="Milliseconds between mousedown and mouseup.")
