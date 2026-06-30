"""
Tests for the Typing Interaction Engine.
"""
import pytest
from nova.intelligence.interaction.typing_engine import TypingEngine
from nova.intelligence.interaction.models import TypingProfile, InteractionConfig

def test_typing_engine_generates_stream():
    engine = TypingEngine(InteractionConfig(typing_profile=TypingProfile.NATURAL))
    
    text = "Hello!"
    stream = engine.generate_typing_stream(text)
    
    assert len(stream) == len(text)
    assert stream[0][0] == "H"
    assert stream[-1][0] == "!"
    
    # Capital 'H' and symbol '!' should have longer delays natively, but we just verify they exist
    for char, delay in stream:
        assert isinstance(delay, float)
        assert delay > 0.0

def test_typing_engine_instant_profile():
    engine = TypingEngine(InteractionConfig(typing_profile=TypingProfile.INSTANT))
    
    text = "Instant Text"
    stream = engine.generate_typing_stream(text)
    
    assert len(stream) == 1
    assert stream[0] == (text, 0.0)
