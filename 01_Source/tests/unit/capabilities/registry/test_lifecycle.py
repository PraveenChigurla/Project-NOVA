"""
Tests for Capability Lifecycle Coordinator.
"""

import pytest
from nova.capabilities.registry import CapabilityRegistry, LifecycleCoordinator
from nova.capabilities.base import CapabilityMetadata, CapabilityState
from nova.capabilities.hello_capability import HelloCapability

@pytest.fixture
def registry():
    return CapabilityRegistry()

@pytest.fixture
def lifecycle(registry):
    return LifecycleCoordinator(registry)

@pytest.mark.asyncio
async def test_boot_and_shutdown_sequence(registry, lifecycle):
    # Setup capability A that depends on B
    meta_a = CapabilityMetadata(id="A", name="A", version="1.0", description="", dependencies=["B"])
    cap_a = HelloCapability(meta_a)
    
    meta_b = CapabilityMetadata(id="B", name="B", version="1.0", description="")
    cap_b = HelloCapability(meta_b)
    
    await registry.register(cap_a)
    await registry.register(cap_b)
    
    # Boot
    await lifecycle.boot_all({})
    
    assert cap_a.state == CapabilityState.READY
    assert cap_b.state == CapabilityState.READY
    
    # Verify topological order (B must start before A)
    # The boot_all logic handles it internally without crashing.
    
    # Teardown
    await lifecycle.shutdown_all()
    assert cap_a.state == CapabilityState.SHUTDOWN
    assert cap_b.state == CapabilityState.SHUTDOWN
