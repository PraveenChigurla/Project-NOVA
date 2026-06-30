"""
Tests for the Optimization Engine.
"""
import pytest
from nova.intelligence.world.chronicle import EventChronicle
from nova.intelligence.optimization.analyzers import ExecutionAnalyzer

def test_execution_analyzer_detects_redundancy():
    chronicle = EventChronicle()
    
    # Simulate 10 executions, 9 of which skipped a step
    for _ in range(10):
        chronicle.record("GoalReceived", {"goal_id": "test_goal"})
        
    for _ in range(9):
        chronicle.record("ExecutionStepSkipped", {"goal_id": "test_goal"})
        
    analyzer = ExecutionAnalyzer()
    proposal = analyzer.analyze_redundancy(chronicle, "test_goal")
    
    assert proposal is not None
    assert proposal.category == "unused_step"
    assert proposal.confidence == 0.9
    assert proposal.requires_approval == True

def test_execution_analyzer_ignores_insufficient_data():
    chronicle = EventChronicle()
    
    # Only 5 executions (less than the 10 required for significance)
    for _ in range(5):
        chronicle.record("GoalReceived", {"goal_id": "test_goal"})
        chronicle.record("ExecutionStepSkipped", {"goal_id": "test_goal"})
        
    analyzer = ExecutionAnalyzer()
    proposal = analyzer.analyze_redundancy(chronicle, "test_goal")
    
    assert proposal is None # Not enough data
