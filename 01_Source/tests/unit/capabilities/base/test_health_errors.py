import pytest
from pydantic import ValidationError
from nova.capabilities.base.health import CapabilityHealth, CapabilityState
from nova.capabilities.base.errors import StructuredError

def test_capability_state_enum():
    """Test the CapabilityState Enum."""
    assert CapabilityState.CREATED == "created"
    assert CapabilityState.READY == "ready"

def test_health_immutability():
    """Test that CapabilityHealth is immutable."""
    health = CapabilityHealth(
        capability_id="com.nova.vision",
        state=CapabilityState.READY,
        is_healthy=True
    )
    assert health.message == "OK"
    with pytest.raises(ValidationError):
        health.is_healthy = False

def test_structured_error():
    """Test StructuredError instantiation and serialization."""
    err = StructuredError(
        error_code="ERR_TEST",
        message="Test error occurred"
    )
    assert err.error_code == "ERR_TEST"
    assert err.recoverable is False
    assert err.capability_id is None
    
    json_data = err.model_dump_json()
    assert "ERR_TEST" in json_data
