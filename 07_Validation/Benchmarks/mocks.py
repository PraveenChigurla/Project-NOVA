import asyncio
from typing import Dict, Any, Callable, Awaitable, Optional
from nova.capabilities.base.capability import Capability
from nova.capabilities.base.metadata import CapabilityMetadata
from nova.capabilities.base.request import CapabilityRequest
from nova.capabilities.base.response import CapabilityResponse
from nova.capabilities.base.context import CapabilityContext

class MockCapability(Capability):
    """A deterministic mock capability for benchmark qualification."""
    
    def __init__(self, capability_id: str, handler: Callable[[CapabilityRequest], Awaitable[Dict[str, Any]]]):
        metadata = CapabilityMetadata(
            id=capability_id,
            name=f"Mock {capability_id}",
            version="1.0.0",
            description=f"Mock capability for {capability_id}",
            author="NOVA EVP",
            supported_intents=["benchmark"],
            permissions_required=[]
        )
        super().__init__(metadata)
        self._handler = handler
        
    async def initialize(self) -> None:
        pass

    async def start(self) -> None:
        pass

    async def execute(self, request: CapabilityRequest, context: Optional[CapabilityContext] = None) -> Dict[str, Any]:
        """Executes the specific mock behavior."""
        return await self._handler(request)

    async def stop(self) -> None:
        pass

    async def shutdown(self) -> None:
        pass

# --- Handlers ---
# The handlers now just return the dictionary data, or raise an exception to simulate failure.
# The `Capability` base class wraps it in a `CapabilityResponse` and catches exceptions.

async def handle_succeed(request: CapabilityRequest) -> Dict[str, Any]:
    delay = request.payload.get("delay_ms", 0)
    if delay > 0:
        await asyncio.sleep(delay / 1000.0)
    return {"status": "mock.succeed"}

async def handle_fail(request: CapabilityRequest) -> Dict[str, Any]:
    raise RuntimeError("Deterministic mock failure")

async def handle_timeout(request: CapabilityRequest) -> Dict[str, Any]:
    # Simulates a capability hanging indefinitely (lowered to 0.05s for stress test viability)
    await asyncio.sleep(0.05)
    return {}

_retry_state = {}
async def handle_retry(request: CapabilityRequest) -> Dict[str, Any]:
    """Fails N times before succeeding."""
    task_id = request.payload.get("task_id", "default")
    required_fails = request.payload.get("fails_required", 2)
    
    current_fails = _retry_state.get(task_id, 0)
    if current_fails < required_fails:
        _retry_state[task_id] = current_fails + 1
        raise RuntimeError("Mock retry failure")
    
    _retry_state[task_id] = 0
    return {"retries_endured": required_fails}

async def handle_rollback(request: CapabilityRequest) -> Dict[str, Any]:
    raise RuntimeError("Mock rollback triggered")

async def handle_permission_denied(request: CapabilityRequest) -> Dict[str, Any]:
    raise PermissionError("Permission denied by mock")

async def handle_provider_failure(request: CapabilityRequest) -> Dict[str, Any]:
    raise RuntimeError("503 Service Unavailable (Mock Provider)")

async def handle_cancel(request: CapabilityRequest) -> Dict[str, Any]:
    try:
        await asyncio.sleep(10.0)
    except asyncio.CancelledError:
        pass
    raise asyncio.CancelledError("Mock cancelled")

# --- Fixtures ---

MOCK_CAPABILITIES = {
    "mock.succeed": MockCapability("mock.succeed", handle_succeed),
    "mock.fail": MockCapability("mock.fail", handle_fail),
    "mock.timeout": MockCapability("mock.timeout", handle_timeout),
    "mock.retry": MockCapability("mock.retry", handle_retry),
    "mock.rollback": MockCapability("mock.rollback", handle_rollback),
    "mock.permission_denied": MockCapability("mock.permission_denied", handle_permission_denied),
    "mock.provider_failure": MockCapability("mock.provider_failure", handle_provider_failure),
    "mock.cancel": MockCapability("mock.cancel", handle_cancel)
}
