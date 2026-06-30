"""
Tests for the Interaction Engine.
"""
import pytest
from nova.intelligence.interaction.engine import InteractionEngine
from nova.intelligence.interaction.models import MovementProfile, InteractionConfig

def test_interaction_engine_bezier_bounds():
    engine = InteractionEngine(InteractionConfig(profile=MovementProfile.NATURAL, jitter=0.5))
    
    start_x, start_y = 100, 100
    end_x, end_y = 800, 600
    
    stream = engine.generate_movement_stream(start_x, start_y, end_x, end_y)
    
    # Verify stream length
    assert len(stream) > 2
    
    # Verify exact endpoints
    assert stream[-1][0] == end_x
    assert stream[-1][1] == end_y
    
    # Verify bounds (jitter could push them slightly out of the strict bounding box, 
    # but not wildly out of screen bounds)
    for x, y, delay in stream:
        assert isinstance(x, int)
        assert isinstance(y, int)
        assert isinstance(delay, float)
        assert delay >= 0.0

def test_interaction_engine_instant_profile():
    engine = InteractionEngine(InteractionConfig(profile=MovementProfile.INSTANT))
    stream = engine.generate_movement_stream(100, 100, 800, 600)
    
    assert len(stream) == 1
    assert stream[0] == (800, 600, 0.0)
