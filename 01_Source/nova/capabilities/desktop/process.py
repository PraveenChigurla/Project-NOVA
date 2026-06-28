"""
Process Capability.
Acts as the intelligence layer for process management.
Translates CapabilityRequests into ProviderRequests.
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

class ProcessCapability(Capability):
    """
    Manages process execution on the host machine safely via the Provider framework.
    """
    
    def __init__(self, metadata, permission_manager: PermissionManager, provider_registry: ProviderRegistry):
        super().__init__(metadata, permission_manager)
        self._provider_registry = provider_registry
        
    async def initialize(self) -> None:
        logger.info(f"[{self.metadata.id}] Initializing Process Capability...")
        
    async def start(self) -> None:
        logger.info(f"[{self.metadata.id}] Process Capability Online.")
        
    async def execute(self, request: CapabilityRequest, context: Optional[CapabilityContext] = None) -> Dict[str, Any]:
        """
        Translates the intent to the Desktop Provider.
        """
        logger.info(f"[{self.metadata.id}] Processing intent: {request.action}")
        
        provider = await self._provider_registry.get("com.nova.provider.desktop")
        if not provider:
            raise RuntimeError("Required Provider 'com.nova.provider.desktop' is not registered!")
            
        # Map Capability Actions to Provider Actions
        # In a more complex system, this involves validation and data transformation.
        prov_req = ProviderRequest(
            provider_id="com.nova.provider.desktop",
            action=request.action,
            payload=request.payload
        )
        
        prov_res = await provider.run(prov_req)
        
        if not prov_res.success:
            raise RuntimeError(f"Provider execution failed: {prov_res.error}")
            
        return prov_res.data
        
    async def stop(self) -> None:
        logger.info(f"[{self.metadata.id}] Process Capability Offline.")
        
    async def shutdown(self) -> None:
        logger.info(f"[{self.metadata.id}] Shutting down.")
