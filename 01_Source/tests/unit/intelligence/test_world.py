"""
Tests for the World Model Graph.
"""
import pytest
from nova.intelligence.world.models import WorldGraph, Entity, Relationship

def test_world_graph_traversal():
    graph = WorldGraph()
    
    app = Entity(id="chrome", type="Application")
    win = Entity(id="win1", type="Window")
    tab = Entity(id="tab1", type="Tab")
    
    graph.add_entity(app)
    graph.add_entity(win)
    graph.add_entity(tab)
    
    graph.add_relationship("chrome", "win1", "contains")
    graph.add_relationship("win1", "tab1", "contains")
    
    # Get entities by type
    apps = graph.get_entities_by_type("Application")
    assert len(apps) == 1
    assert apps[0].id == "chrome"
    
    # Traversal
    chrome_children = graph.get_related("chrome", rel_type="contains")
    assert len(chrome_children) == 1
    assert chrome_children[0].id == "win1"
    
def test_world_graph_missing_entities():
    graph = WorldGraph()
    
    app = Entity(id="chrome", type="Application")
    graph.add_entity(app)
    
    # Try adding a relationship to a non-existent entity
    graph.add_relationship("chrome", "nonexistent", "contains")
    
    assert len(graph.relationships) == 0
