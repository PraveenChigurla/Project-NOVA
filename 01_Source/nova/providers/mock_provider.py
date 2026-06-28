"""
Mock Provider Demonstration.
A minimal implementation of the Provider Framework ABC to serve as a reference.
"""

from typing import Dict, Any, Optional
import logging

from nova.providers.base import (
    Provider,
    ProviderRequest,
    ProviderContext
)

logger = logging.getLogger(__name__)

class MockProvider(Provider):
    """
    A minimal reference implementation of a NOVA Provider.
    Simulates a hardware or external API connection.
    """
    
    async def initialize(self) -> None:
        logger.info(f"[{self.metadata.id}] Initializing Mock Hardware/API with config: {self._config}")
        
    async def start(self) -> None:
        logger.info(f"[{self.metadata.id}] Connecting to Mock API...")
        
    async def execute(self, request: ProviderRequest, context: Optional[ProviderContext] = None) -> Dict[str, Any]:
        logger.info(f"[{self.metadata.id}] Executing mock action: {request.action}")
        
        if request.action == "ping":
            return {"status": "pong"}
            
        return {"error": "Unknown action"}
        
    async def stop(self) -> None:
        logger.info(f"[{self.metadata.id}] Disconnecting Mock API...")
        
    async def shutdown(self) -> None:
        logger.info(f"[{self.metadata.id}] Shutting down Mock Provider...")
