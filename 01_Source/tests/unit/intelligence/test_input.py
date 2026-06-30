"""
Tests for the Input Framework.
"""
import pytest
from nova.intelligence.input.models import NormalizedInput
from nova.intelligence.input.normalizer import InputNormalizer
from nova.intelligence.input.conversation import ConversationManager

def test_input_normalizer_cleans_text():
    normalizer = InputNormalizer()
    
    raw = NormalizedInput(
        text="   open chrome   ",
        source="cli",
        session_id="123",
        confidence=1.0
    )
    
    norm = normalizer.normalize(raw)
    assert norm.text == "Open chrome"

def test_input_normalizer_rejects_low_confidence():
    normalizer = InputNormalizer()
    
    raw = NormalizedInput(
        text="open chrome",
        source="voice",
        session_id="123",
        confidence=0.2 # Too low
    )
    
    norm = normalizer.normalize(raw)
    assert norm.text == ""

def test_conversation_manager_tracks_history():
    manager = ConversationManager()
    
    input1 = NormalizedInput(text="First", source="cli", session_id="session_A")
    input2 = NormalizedInput(text="Second", source="cli", session_id="session_A")
    input3 = NormalizedInput(text="Other", source="cli", session_id="session_B")
    
    manager.process(input1)
    manager.process(input2)
    manager.process(input3)
    
    assert len(manager.history["session_A"]) == 2
    assert len(manager.history["session_B"]) == 1
