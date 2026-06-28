"""
HelloCapability Demonstration.
A minimal implementation of the Capability Framework ABC to serve as a reference.
"""

from typing import Dict, Any, Optional
import logging

from nova.capabilities.base import (
    Capability,
    CapabilityRequest,
    CapabilityContext
)
from nova.security.permissions import PermissionManager, PermissionRequest, PermissionScope

logger = logging.getLogger(__name__)

class HelloCapability(Capability):
    """
    A minimal reference implementation of a NOVA Capability.
    """
    
    def __init__(self, metadata, permission_manager: Optional[PermissionManager] = None):
        super().__init__(metadata)
        self.permission_manager = permission_manager
    
    async def initialize(self) -> None:
        """Parse configuration and set up initial state."""
        logger.info(f"[{self.metadata.id}] Initializing with config: {self._config}")
        
    async def start(self) -> None:
        """Bind to event bus and prepare to receive requests."""
        logger.info(f"[{self.metadata.id}] Starting capability...")
        
    async def execute(self, request: CapabilityRequest, context: Optional[CapabilityContext] = None) -> Dict[str, Any]:
        """The core execution logic."""
        logger.info(f"[{self.metadata.id}] Executing action: {request.action}")
        
        if request.action == "say_hello":
            name = request.payload.get("name", "World")
            return {"message": f"Hello, {name}!"}
            
        elif request.action == "read_file":
            if not self.permission_manager:
                raise ValueError("PermissionManager not injected!")
                
            perm_req = PermissionRequest(
                capability_id=self.metadata.id,
                scope=PermissionScope.OS_FILES_READ,
                context={"path": request.payload.get("path")}
            )
            result = await self.permission_manager.evaluate(perm_req)
            if not result.is_allowed:
                raise PermissionError(f"Permission denied: {result.message}")
                
            return {"content": "Simulated file content read successfully."}
            
        elif request.action == "cause_error":
            raise ValueError("This is a simulated capability crash!")
            
        return {"error": "Unknown action"}
        
    async def stop(self) -> None:
        """Pause operations."""
        logger.info(f"[{self.metadata.id}] Stopping capability...")
        
    async def shutdown(self) -> None:
        """Tear down resources."""
        logger.info(f"[{self.metadata.id}] Shutting down...")

    # -------------------------------------------------------------------------
    # Optional Hooks Demonstration
    # -------------------------------------------------------------------------
    
    async def before_execute(self, request: CapabilityRequest) -> None:
        logger.debug(f"[{self.metadata.id}] Hook: before_execute fired for {request.id}")
        
    async def after_execute(self, response: Any) -> None:
        logger.debug(f"[{self.metadata.id}] Hook: after_execute fired. Success: {response.success}")
