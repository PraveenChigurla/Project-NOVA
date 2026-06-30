"""
Screen Capability (Temporary Mock for Phase 2, Sprint 9).
Pass-through intelligence layer for Screen Capture.
"""

from typing import Dict, Any, Optional
import logging

from nova.capabilities.base import (
    Capability,
    CapabilityRequest,
    CapabilityResponse,
    CapabilityContext
)
from nova.security.permissions import PermissionManager
from nova.providers.registry.registry import ProviderRegistry
from nova.providers.base import ProviderRequest

logger = logging.getLogger(__name__)

class ScreenCapability(Capability):
    """
    Temporary capability to pass capture requests to the Screen Capture Provider.
    In future sprints, this will house OCR and Computer Vision logic.
    """
    
    def __init__(self, metadata, permission_manager: PermissionManager, provider_registry: ProviderRegistry):
        super().__init__(metadata, permission_manager)
        self._provider_registry = provider_registry
        
    async def initialize(self) -> None:
        logger.info(f"[{self.metadata.id}] Initializing Screen Capability...")
        
    async def start(self) -> None:
        logger.info(f"[{self.metadata.id}] Screen Capability Online.")
        
    async def execute(self, request: CapabilityRequest, context: Optional[CapabilityContext] = None) -> Dict[str, Any]:
        """
        Translates the intent to the Screen Capture Provider.
        """
        logger.info(f"[{self.metadata.id}] Processing intent: {request.action}")
        
        provider = await self._provider_registry.get("com.nova.provider.screen")
        if not provider:
            raise RuntimeError("Required Provider 'com.nova.provider.screen' is not registered!")
            
        prov_req = ProviderRequest(
            provider_id="com.nova.provider.screen",
            action=request.action,
            payload=request.payload
        )
        
        prov_res = await provider.run(prov_req)
        
        if not prov_res.success:
            raise RuntimeError(f"Provider execution failed: {prov_res.error}")
            
        return prov_res.data
        
    async def stop(self) -> None:
        logger.info(f"[{self.metadata.id}] Screen Capability Offline.")
        
    async def shutdown(self) -> None:
        logger.info(f"[{self.metadata.id}] Shutting down.")
