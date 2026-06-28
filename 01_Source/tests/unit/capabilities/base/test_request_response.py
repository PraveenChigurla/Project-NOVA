import pytest
from pydantic import ValidationError
from nova.capabilities.base.request import CapabilityRequest
from nova.capabilities.base.response import CapabilityResponse

def test_request_auto_generation():
    """Test that ID and timestamp are auto-generated."""
    req = CapabilityRequest(
        capability_id="com.nova.vision",
        action="capture"
    )
    assert req.id is not None
    assert req.timestamp is not None
    assert req.payload == {}

def test_request_immutability():
    """Test that CapabilityRequest is immutable."""
    req = CapabilityRequest(
        capability_id="com.nova.vision",
        action="capture"
    )
    with pytest.raises(ValidationError):
        req.action = "new_action"

def test_response_validation():
    """Test valid CapabilityResponse."""
    resp = CapabilityResponse(
        request_id="req-123",
        capability_id="com.nova.vision",
        success=True,
        data={"result": "ok"},
        elapsed_ms=42.5
    )
    assert resp.request_id == "req-123"
    assert resp.success is True
    assert resp.data["result"] == "ok"
    assert resp.error is None

def test_response_immutability():
    """Test that CapabilityResponse is immutable."""
    resp = CapabilityResponse(
        request_id="req-123",
        capability_id="com.nova.vision",
        success=True,
        elapsed_ms=42.5
    )
    with pytest.raises(ValidationError):
        resp.success = False
