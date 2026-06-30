"""
Tests for the Cognitive Pipeline.
"""
import pytest
from nova.intelligence.cognition.engines.constraint_engine import ConstraintEngine
from nova.intelligence.cognition.models import ContextSnapshot, WorldState
import time

def test_constraint_engine_weekend_rule():
    engine = ConstraintEngine()
    
    # Mock a weekend context
    context = ContextSnapshot(
        timestamp=time.time(),
        iso_date="2026-06-28",
        day_of_week="Sunday",
        hour=14,
        timezone="UTC"
    )
    
    state = WorldState(active_processes=[])
    
    report = engine.evaluate(context, state)
    
    assert report.ask_user_confirmation == True
    assert report.skip_heavy_apps == True
    assert len(report.reasons) == 1
    assert "Weekend" in report.reasons[0]

def test_constraint_engine_quiet_hours_rule():
    engine = ConstraintEngine()
    
    # Mock a late night context
    context = ContextSnapshot(
        timestamp=time.time(),
        iso_date="2026-06-29",
        day_of_week="Monday",
        hour=23,
        timezone="UTC"
    )
    
    state = WorldState(active_processes=[])
    
    report = engine.evaluate(context, state)
    
    assert report.ask_user_confirmation == True
    assert len(report.reasons) == 1
    assert "Quiet hours" in report.reasons[0]
