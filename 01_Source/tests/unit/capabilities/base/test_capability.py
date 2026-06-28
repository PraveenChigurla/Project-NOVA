import pytest
from nova.capabilities.base import (
    CapabilityMetadata, 
    CapabilityState, 
    CapabilityRequest,
    InvalidStateTransitionError
)
from nova.capabilities.hello_capability import HelloCapability

@pytest.fixture
def hello_cap():
    meta = CapabilityMetadata(
        id="com.nova.hello",
        name="Hello Demo",
        version="1.0.0",
        description="Demo"
    )
    return HelloCapability(meta)

@pytest.mark.asyncio
async def test_capability_valid_lifecycle(hello_cap):
    """Test the complete happy path lifecycle."""
    assert hello_cap.state == CapabilityState.CREATED
    
    await hello_cap.system_register()
    assert hello_cap.state == CapabilityState.REGISTERED
    
    await hello_cap.system_initialize({"setting": True})
    assert hello_cap.state == CapabilityState.INITIALIZED
    
    await hello_cap.system_start()
    assert hello_cap.state == CapabilityState.READY
    
    # Execute
    req = CapabilityRequest(capability_id="com.nova.hello", action="say_hello", payload={"name": "Alice"})
    resp = await hello_cap.run(req)
    
    assert resp.success is True
    assert resp.data["message"] == "Hello, Alice!"
    assert hello_cap.state == CapabilityState.IDLE
    
    await hello_cap.system_stop()
    assert hello_cap.state == CapabilityState.STOPPED
    
    await hello_cap.system_shutdown()
    assert hello_cap.state == CapabilityState.SHUTDOWN


@pytest.mark.asyncio
async def test_capability_invalid_transition(hello_cap):
    """Test that skipping states raises an error."""
    assert hello_cap.state == CapabilityState.CREATED
    
    with pytest.raises(InvalidStateTransitionError):
        # Cannot start before initializing
        await hello_cap.system_start()

@pytest.mark.asyncio
async def test_capability_error_handling(hello_cap):
    """Test that errors in execute() are caught and turned into StructuredErrors."""
    await hello_cap.system_register()
    await hello_cap.system_initialize({})
    await hello_cap.system_start()
    
    # Trigger the simulated crash
    req = CapabilityRequest(capability_id="com.nova.hello", action="cause_error")
    resp = await hello_cap.run(req)
    
    assert resp.success is False
    assert resp.error is not None
    assert resp.error["error_code"] == "ERR_CAP_EXECUTION"
    assert "simulated capability crash" in resp.error["message"]
    
    # Ensure we return to IDLE after catching the error
    assert hello_cap.state == CapabilityState.IDLE
