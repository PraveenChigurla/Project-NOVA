"""
Tests for Capability Registry.
"""

import pytest
import asyncio
from nova.capabilities.registry.registry import CapabilityRegistry, CapabilityRegistryError
from nova.capabilities.base import CapabilityMetadata, CapabilityState
from nova.capabilities.hello_capability import HelloCapability

@pytest.fixture
def registry():
    return CapabilityRegistry()

@pytest.fixture
def mock_capability():
    meta = CapabilityMetadata(
        id="com.nova.test",
        name="Test Cap",
        version="1.0.0",
        description="test",
        tags=["system"],
        supported_intents=["do_test"],
        permissions_required=["os.read"]
    )
    return HelloCapability(meta)

@pytest.mark.asyncio
async def test_register_and_lookup(registry, mock_capability):
    await registry.register(mock_capability)
    
    assert mock_capability.state == CapabilityState.REGISTERED
    
    # Lookup
    found = await registry.get("com.nova.test")
    assert found is not None
    assert found.metadata.name == "Test Cap"
    
    # Test queries
    assert len(await registry.get_by_tag("system")) == 1
    assert len(await registry.get_by_intent("do_test")) == 1
    assert len(await registry.get_by_permission("os.read")) == 1

@pytest.mark.asyncio
async def test_duplicate_registration(registry, mock_capability):
    await registry.register(mock_capability)
    
    with pytest.raises(CapabilityRegistryError, match="already registered"):
        await registry.register(mock_capability)

@pytest.mark.asyncio
async def test_concurrent_registration():
    registry = CapabilityRegistry()
    
    async def register_cap(i):
        meta = CapabilityMetadata(id=f"cap_{i}", name=f"Name {i}", version="1.0", description="")
        cap = HelloCapability(meta)
        await registry.register(cap)
        
    await asyncio.gather(*(register_cap(i) for i in range(10)))
    
    caps = await registry.enumerate_capabilities()
    assert len(caps) == 10
