"""
Tests for the Cognitive Federation Runtime.
"""
import pytest
from nova.intelligence.llm.models import GoalContract
from nova.federation.models import NodeIdentity, CapabilityAdvertisement
from nova.federation.registry import NodeRegistry
from nova.federation.router import GoalRouter

def test_router_handles_local_goal():
    identity = NodeIdentity(node_id="local")
    registry = NodeRegistry(identity)
    router = GoalRouter(["browser", "vscode"], registry)
    
    goal = GoalContract(
        goal_id="test",
        target_state="test",
        required_capabilities=["browser"],
        requires_confirmation=False
    )
    
    # Should return None, meaning "handle locally"
    target = router.determine_target_node(goal)
    assert target is None

def test_router_delegates_to_peer():
    identity = NodeIdentity(node_id="local")
    registry = NodeRegistry(identity)
    
    # Register a peer
    peer_ad = CapabilityAdvertisement(
        node=NodeIdentity(node_id="remote_server"),
        capabilities=["gpu"]
    )
    registry.register_peer_advertisement(peer_ad)
    
    router = GoalRouter(["browser"], registry)
    
    goal = GoalContract(
        goal_id="test",
        target_state="test",
        required_capabilities=["gpu"],
        requires_confirmation=False
    )
    
    # Should return the remote server node
    target = router.determine_target_node(goal)
    assert target is not None
    assert target.node_id == "remote_server"

def test_router_fails_if_capability_missing_entirely():
    identity = NodeIdentity(node_id="local")
    registry = NodeRegistry(identity)
    
    router = GoalRouter(["browser"], registry)
    
    goal = GoalContract(
        goal_id="test",
        target_state="test",
        required_capabilities=["quantum_compute"], # No one has this
        requires_confirmation=False
    )
    
    with pytest.raises(RuntimeError):
        router.determine_target_node(goal)
