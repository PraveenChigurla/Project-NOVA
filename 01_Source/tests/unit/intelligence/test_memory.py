"""
Tests for the Memory Subsystems.
"""
import pytest
from nova.intelligence.memory.manager import MemoryManager
from nova.intelligence.memory.models import Fact, Episode

def test_memory_manager_working_clear():
    mgr = MemoryManager()
    mgr.working.set("test_key", "test_val")
    assert mgr.working.get("test_key") == "test_val"
    
    mgr.initialize_session()
    assert mgr.working.get("test_key") is None
    
def test_memory_manager_snapshot():
    mgr = MemoryManager()
    
    # Store Semantic
    mgr.semantic.store_fact(Fact(key="color", value="blue"))
    
    # Store Episodic
    mgr.episodic.record(Episode(goal_id="test", success=True, summary="Testing"))
    
    # Build Snapshot
    snapshot = mgr.build_snapshot("test")
    
    assert len(snapshot.relevant_facts) == 1
    assert snapshot.relevant_facts[0].value == "blue"
    
    assert len(snapshot.recent_episodes) == 1
    assert snapshot.recent_episodes[0].success == True
