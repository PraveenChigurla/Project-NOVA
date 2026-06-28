"""
Capability Abstract Base Class.
Defines the runtime contract for all capabilities in Project NOVA.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from datetime import datetime, timezone
import time
import logging

from nova.capabilities.base.metadata import CapabilityMetadata
from nova.capabilities.base.request import CapabilityRequest
from nova.capabilities.base.response import CapabilityResponse
from nova.capabilities.base.context import CapabilityContext
from nova.capabilities.base.health import CapabilityState, CapabilityHealth
from nova.capabilities.base.errors import StructuredError

logger = logging.getLogger(__name__)

class InvalidStateTransitionError(Exception):
    """Raised when a capability attempts an illegal state transition."""
    pass

class Capability(ABC):
    """
    Abstract base class that defines the runtime contract for every capability.
    """
    
    # Valid state transitions matrix
    _VALID_TRANSITIONS = {
        CapabilityState.CREATED: [CapabilityState.REGISTERED],
        CapabilityState.REGISTERED: [CapabilityState.INITIALIZED, CapabilityState.SHUTDOWN],
        CapabilityState.INITIALIZED: [CapabilityState.STARTED, CapabilityState.SHUTDOWN],
        CapabilityState.STARTED: [CapabilityState.READY, CapabilityState.STOPPING],
        CapabilityState.READY: [CapabilityState.EXECUTING, CapabilityState.IDLE, CapabilityState.STOPPING],
        CapabilityState.EXECUTING: [CapabilityState.READY, CapabilityState.IDLE, CapabilityState.STOPPING],
        CapabilityState.IDLE: [CapabilityState.EXECUTING, CapabilityState.READY, CapabilityState.STOPPING],
        CapabilityState.STOPPING: [CapabilityState.STOPPED],
        CapabilityState.STOPPED: [CapabilityState.SHUTDOWN],
        CapabilityState.SHUTDOWN: []
    }

    def __init__(self, metadata: CapabilityMetadata):
        self._metadata = metadata
        self._state = CapabilityState.CREATED
        self._config: Optional[Dict[str, Any]] = None
        # In a real system, these would be injected by the Registry:
        # self._event_bus = event_bus
        # self._logger = logger
        
    @property
    def metadata(self) -> CapabilityMetadata:
        return self._metadata
        
    @property
    def state(self) -> CapabilityState:
        return self._state

    def _transition_state(self, new_state: CapabilityState) -> None:
        """
        Enforce valid state transitions.
        """
        if new_state not in self._VALID_TRANSITIONS[self._state]:
            raise InvalidStateTransitionError(
                f"Cannot transition {self.metadata.id} from {self._state.value} to {new_state.value}"
            )
        logger.debug(f"Capability {self.metadata.id} transitioning: {self._state.value} -> {new_state.value}")
        self._state = new_state

    # -------------------------------------------------------------------------
    # Core Abstract Methods (Must be implemented by subclasses)
    # -------------------------------------------------------------------------

    @abstractmethod
    async def initialize(self) -> None:
        """Called after registration. Inject dependencies and parse config here."""
        pass

    @abstractmethod
    async def start(self) -> None:
        """Called to bind to the Event Bus and prepare for execution."""
        pass

    @abstractmethod
    async def execute(self, request: CapabilityRequest, context: Optional[CapabilityContext] = None) -> Dict[str, Any]:
        """The core execution logic. Should return a dictionary payload."""
        pass

    @abstractmethod
    async def stop(self) -> None:
        """Called to pause operations or prepare for shutdown."""
        pass

    @abstractmethod
    async def shutdown(self) -> None:
        """Called to free resources permanently."""
        pass

    # -------------------------------------------------------------------------
    # Optional Lifecycle Hooks
    # -------------------------------------------------------------------------

    async def before_execute(self, request: CapabilityRequest) -> None:
        """Optional hook fired before execute()."""
        pass

    async def after_execute(self, response: CapabilityResponse) -> None:
        """Optional hook fired after a successful execute()."""
        pass

    async def on_error(self, error: StructuredError) -> None:
        """Optional hook fired when an error occurs during run()."""
        pass

    async def on_health_check(self) -> CapabilityHealth:
        """
        Default health check hook. Subclasses can override to perform
        deep system checks.
        """
        return CapabilityHealth(
            capability_id=self.metadata.id,
            state=self.state,
            is_healthy=True,
            message="OK"
        )

    # -------------------------------------------------------------------------
    # System Execution Entry Point (Template Method)
    # -------------------------------------------------------------------------

    async def run(self, request: CapabilityRequest, context: Optional[CapabilityContext] = None) -> CapabilityResponse:
        """
        The Template Method for execution.
        Enforces state transitions, calls hooks, and catches errors.
        """
        if self._state not in (CapabilityState.READY, CapabilityState.IDLE):
            raise InvalidStateTransitionError(
                f"Capability {self.metadata.id} must be in READY or IDLE state to execute (currently {self._state.value})"
            )
            
        start_time = time.perf_counter()
        
        try:
            self._transition_state(CapabilityState.EXECUTING)
            
            await self.before_execute(request)
            result_data = await self.execute(request, context)
            
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            
            response = CapabilityResponse(
                request_id=request.id,
                capability_id=self.metadata.id,
                success=True,
                data=result_data,
                elapsed_ms=elapsed_ms
            )
            
            await self.after_execute(response)
            
            self._transition_state(CapabilityState.IDLE)
            return response
            
        except Exception as e:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            error = StructuredError(
                error_code="ERR_CAP_EXECUTION",
                capability_id=self.metadata.id,
                message=str(e),
                recoverable=False
            )
            
            await self.on_error(error)
            
            # Transition to IDLE if we recover, else we might go to STOPPING.
            # For this simple base class, we just return to IDLE so the framework can decide.
            self._transition_state(CapabilityState.IDLE)
            
            return CapabilityResponse(
                request_id=request.id,
                capability_id=self.metadata.id,
                success=False,
                data={},
                error=error.model_dump(),
                elapsed_ms=elapsed_ms
            )

    # -------------------------------------------------------------------------
    # Framework System Methods (Called by Registry)
    # -------------------------------------------------------------------------
    
    async def system_register(self) -> None:
        self._transition_state(CapabilityState.REGISTERED)
        
    async def system_initialize(self, config: Dict[str, Any]) -> None:
        self._transition_state(CapabilityState.INITIALIZED)
        self._config = config
        await self.initialize()
        
    async def system_start(self) -> None:
        self._transition_state(CapabilityState.STARTED)
        await self.start()
        self._transition_state(CapabilityState.READY)
        
    async def system_stop(self) -> None:
        self._transition_state(CapabilityState.STOPPING)
        await self.stop()
        self._transition_state(CapabilityState.STOPPED)
        
    async def system_shutdown(self) -> None:
        # If not stopped, force stop
        if self._state != CapabilityState.STOPPED:
            await self.system_stop()
        await self.shutdown()
        self._transition_state(CapabilityState.SHUTDOWN)
