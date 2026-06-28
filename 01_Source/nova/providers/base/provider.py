"""
Provider Abstract Base Class.
Defines the runtime contract for all providers in Project NOVA.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import time
import logging

from nova.providers.base.models import (
    ProviderMetadata,
    ProviderRequest,
    ProviderResponse,
    ProviderContext,
    ProviderState,
    ProviderHealth,
    ProviderError
)

logger = logging.getLogger(__name__)

class InvalidProviderStateError(Exception):
    """Raised when a provider attempts an illegal state transition."""
    pass

class Provider(ABC):
    """
    Abstract base class that defines the runtime contract for every provider.
    """
    
    # Valid state transitions matrix (Identical to Capabilities)
    _VALID_TRANSITIONS = {
        ProviderState.CREATED: [ProviderState.REGISTERED],
        ProviderState.REGISTERED: [ProviderState.INITIALIZED, ProviderState.SHUTDOWN],
        ProviderState.INITIALIZED: [ProviderState.STARTED, ProviderState.SHUTDOWN],
        ProviderState.STARTED: [ProviderState.READY, ProviderState.STOPPING],
        ProviderState.READY: [ProviderState.EXECUTING, ProviderState.IDLE, ProviderState.STOPPING],
        ProviderState.EXECUTING: [ProviderState.READY, ProviderState.IDLE, ProviderState.STOPPING],
        ProviderState.IDLE: [ProviderState.EXECUTING, ProviderState.READY, ProviderState.STOPPING],
        ProviderState.STOPPING: [ProviderState.STOPPED],
        ProviderState.STOPPED: [ProviderState.SHUTDOWN],
        ProviderState.SHUTDOWN: []
    }

    def __init__(self, metadata: ProviderMetadata):
        self._metadata = metadata
        self._state = ProviderState.CREATED
        self._config: Optional[Dict[str, Any]] = None
        
    @property
    def metadata(self) -> ProviderMetadata:
        return self._metadata
        
    @property
    def state(self) -> ProviderState:
        return self._state

    def _transition_state(self, new_state: ProviderState) -> None:
        """Enforce valid state transitions."""
        if new_state not in self._VALID_TRANSITIONS[self._state]:
            raise InvalidProviderStateError(
                f"Cannot transition {self.metadata.id} from {self._state.value} to {new_state.value}"
            )
        logger.debug(f"Provider {self.metadata.id} transitioning: {self._state.value} -> {new_state.value}")
        self._state = new_state

    # -------------------------------------------------------------------------
    # Core Abstract Methods
    # -------------------------------------------------------------------------

    @abstractmethod
    async def initialize(self) -> None:
        pass

    @abstractmethod
    async def start(self) -> None:
        pass

    @abstractmethod
    async def execute(self, request: ProviderRequest, context: Optional[ProviderContext] = None) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def stop(self) -> None:
        pass

    @abstractmethod
    async def shutdown(self) -> None:
        pass

    # -------------------------------------------------------------------------
    # Optional Hooks
    # -------------------------------------------------------------------------

    async def before_execute(self, request: ProviderRequest) -> None:
        pass

    async def after_execute(self, response: ProviderResponse) -> None:
        pass

    async def on_error(self, error: ProviderError) -> None:
        pass

    async def on_health_check(self) -> ProviderHealth:
        return ProviderHealth(
            provider_id=self.metadata.id,
            state=self.state,
            is_healthy=True,
            message="OK"
        )

    # -------------------------------------------------------------------------
    # System Execution Entry Point (Template Method)
    # -------------------------------------------------------------------------

    async def run(self, request: ProviderRequest, context: Optional[ProviderContext] = None) -> ProviderResponse:
        """The Template Method for execution."""
        if self._state not in (ProviderState.READY, ProviderState.IDLE):
            raise InvalidProviderStateError(
                f"Provider {self.metadata.id} must be in READY or IDLE state to execute (currently {self._state.value})"
            )
            
        start_time = time.perf_counter()
        
        try:
            self._transition_state(ProviderState.EXECUTING)
            
            await self.before_execute(request)
            result_data = await self.execute(request, context)
            
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            
            response = ProviderResponse(
                request_id=request.id,
                provider_id=self.metadata.id,
                success=True,
                data=result_data,
                elapsed_ms=elapsed_ms
            )
            
            await self.after_execute(response)
            
            self._transition_state(ProviderState.IDLE)
            return response
            
        except Exception as e:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            error = ProviderError(
                error_code="ERR_PROV_EXECUTION",
                provider_id=self.metadata.id,
                message=str(e),
                recoverable=False
            )
            
            await self.on_error(error)
            self._transition_state(ProviderState.IDLE)
            
            return ProviderResponse(
                request_id=request.id,
                provider_id=self.metadata.id,
                success=False,
                data={},
                error=error.model_dump(),
                elapsed_ms=elapsed_ms
            )

    # -------------------------------------------------------------------------
    # Framework System Methods
    # -------------------------------------------------------------------------
    
    async def system_register(self) -> None:
        self._transition_state(ProviderState.REGISTERED)
        
    async def system_initialize(self, config: Dict[str, Any]) -> None:
        self._transition_state(ProviderState.INITIALIZED)
        self._config = config
        await self.initialize()
        
    async def system_start(self) -> None:
        self._transition_state(ProviderState.STARTED)
        await self.start()
        self._transition_state(ProviderState.READY)
        
    async def system_stop(self) -> None:
        self._transition_state(ProviderState.STOPPING)
        await self.stop()
        self._transition_state(ProviderState.STOPPED)
        
    async def system_shutdown(self) -> None:
        if self._state != ProviderState.STOPPED:
            await self.system_stop()
        await self.shutdown()
        self._transition_state(ProviderState.SHUTDOWN)
