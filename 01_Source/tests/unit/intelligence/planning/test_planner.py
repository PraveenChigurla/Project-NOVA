"""
Tests for the Planner Framework and TaskGraph.
"""

import pytest
from nova.intelligence.planning.models import PlanStep
from nova.intelligence.planning.graph import TaskGraph, CircularDependencyError, MissingDependencyError
from nova.intelligence.planning.planner import RuleBasedPlanner

def test_task_graph_missing_dependency():
    step1 = PlanStep(capability_id="test", action="act", dependencies=["non_existent_step"])
    graph = TaskGraph([step1])
    
    with pytest.raises(MissingDependencyError):
        graph.validate()

def test_task_graph_circular_dependency():
    step1 = PlanStep(step_id="1", capability_id="test", action="act", dependencies=["2"])
    step2 = PlanStep(step_id="2", capability_id="test", action="act", dependencies=["1"])
    
    graph = TaskGraph([step1, step2])
    
    with pytest.raises(CircularDependencyError):
        graph.validate()

def test_task_graph_layer_resolution():
    # A -> B -> D
    # C -> D
    step_a = PlanStep(step_id="A", capability_id="test", action="act", dependencies=[])
    step_b = PlanStep(step_id="B", capability_id="test", action="act", dependencies=["A"])
    step_c = PlanStep(step_id="C", capability_id="test", action="act", dependencies=[])
    step_d = PlanStep(step_id="D", capability_id="test", action="act", dependencies=["B", "C"])
    
    graph = TaskGraph([step_a, step_b, step_c, step_d])
    layers = graph.get_execution_layers()
    
    assert len(layers) == 3
    # Layer 0 should be A and C
    layer_0_ids = {s.step_id for s in layers[0]}
    assert layer_0_ids == {"A", "C"}
    
    # Layer 1 should be B
    layer_1_ids = {s.step_id for s in layers[1]}
    assert layer_1_ids == {"B"}
    
    # Layer 2 should be D
    layer_2_ids = {s.step_id for s in layers[2]}
    assert layer_2_ids == {"D"}

@pytest.mark.asyncio
async def test_rule_based_planner():
    planner = RuleBasedPlanner()
    
    # Test unknown intent
    res1 = await planner.plan("Do some random thing")
    assert res1.success is False
    assert "does not understand" in res1.error_message
    
    # Test valid intent
    res2 = await planner.plan("Open Chrome")
    assert res2.success is True
    assert res2.plan is not None
    assert len(res2.plan.steps) == 1
    assert res2.plan.steps[0].action == "launch_application"
