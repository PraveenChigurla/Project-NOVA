"""
Tests for the Provider Framework.
"""

import pytest
import asyncio
from nova.providers.base import (
    ProviderType,
    ProviderState,
    ProviderMetadata,
    ProviderRequest,
    InvalidProviderStateError
)
from nova.providers.mock_provider import MockProvider
from nova.providers.registry.registry import ProviderRegistry, ProviderRegistryError

@pytest.fixture
def metadata():
    return ProviderMetadata(
        id="com.nova.test_prov",
        name="Test Provider",
        version="1.0.0",
        type=ProviderType.MOCK,
        description="A test provider"
    )

@pytest.fixture
def provider(metadata):
    return MockProvider(metadata)

@pytest.fixture
def registry():
    return ProviderRegistry()

@pytest.mark.asyncio
async def test_provider_state_transitions(provider):
    # Initial state
    assert provider.state == ProviderState.CREATED
    
    # Must register before init
    await provider.system_register()
    assert provider.state == ProviderState.REGISTERED
    
    await provider.system_initialize({})
    assert provider.state == ProviderState.INITIALIZED
    
    await provider.system_start()
    assert provider.state == ProviderState.READY
    
    # Execution transition
    req = ProviderRequest(provider_id=provider.metadata.id, action="ping")
    res = await provider.run(req)
    assert res.success is True
    assert res.data["status"] == "pong"
    # Returns to IDLE after execution
    assert provider.state == ProviderState.IDLE
    
    # Shutdown
    await provider.system_shutdown()
    assert provider.state == ProviderState.SHUTDOWN

@pytest.mark.asyncio
async def test_provider_invalid_transition(provider):
    with pytest.raises(InvalidProviderStateError):
        # Cannot execute if not in READY or IDLE
        req = ProviderRequest(provider_id=provider.metadata.id, action="ping")
        await provider.run(req)

@pytest.mark.asyncio
async def test_registry_duplicate_registration(registry, provider):
    await registry.register(provider)
    
    with pytest.raises(ProviderRegistryError, match="already registered"):
        await registry.register(provider)

@pytest.mark.asyncio
async def test_registry_lookup(registry, provider):
    await registry.register(provider)
    
    found = await registry.get(provider.metadata.id)
    assert found is not None
    assert found.metadata.name == "Test Provider"
    
    by_type = await registry.get_by_type(ProviderType.MOCK)
    assert len(by_type) == 1
