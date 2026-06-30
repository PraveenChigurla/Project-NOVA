"""
Keyboard Capability.
Orchestrates human-like typing using the Typing Engine and Keyboard Provider.
"""
import asyncio
import logging
from typing import Dict, Any, Optional

from nova.capabilities.base import Capability, CapabilityMetadata, CapabilityType
from nova.security.permissions.models import PermissionScope
from nova.providers.base import ProviderRequest
from nova.intelligence.interaction.typing_engine import TypingEngine, TypingProfile

logger = logging.getLogger(__name__)

class KeyboardCapability(Capability):
    """Execution bridge mapping Planner intents to human-like typing streams."""
    
    def __init__(self, metadata: CapabilityMetadata):
        super().__init__(metadata)
        self.typing_engine = TypingEngine()
        
    async def initialize(self) -> None:
        logger.info(f"[{self.metadata.id}] Initializing Keyboard Capability...")
        
    async def execute(self, action: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes a semantic typing action.
        Supports: 'type_human'
        """
        if not self.kernel:
            raise RuntimeError("KeyboardCapability requires Kernel attachment.")
            
        provider = self.kernel.provider_registry.get("com.nova.provider.keyboard")
        if not provider:
            raise RuntimeError("Required provider 'com.nova.provider.keyboard' not found.")
            
        logger.debug(f"[{self.metadata.id}] Executing semantic action: {action}")
        
        if action == "type_human":
            # 1. Permission Check
            await self.kernel.permission_manager.request(
                self.metadata.id, PermissionScope.OS_KEYBOARD_PRESS, "Type text to active window."
            )
            
            return await self._execute_human_typing(provider, parameters)
            
        raise ValueError(f"Unknown action: {action}")
        
    async def _execute_human_typing(self, provider, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Generates a timed character stream and sequentially dispatches it."""
        text = parameters.get("text", "")
        profile_str = parameters.get("profile", "natural")
        
        try:
            profile = TypingProfile(profile_str)
        except ValueError:
            profile = TypingProfile.NATURAL
            
        # Generate mathematical stream
        stream = self.typing_engine.generate_typing_stream(text, profile)
        
        logger.info(f"[{self.metadata.id}] Dispatched {profile.value} typing stream for {len(stream)} characters.")
        
        # Execute the stream natively
        for char, delay_sec in stream:
            # We send characters one by one via the native provider to respect the timing
            req = ProviderRequest(action="type_text", payload={"text": char})
            await provider.execute(req)
            
            if delay_sec > 0:
                await asyncio.sleep(delay_sec)
                
        return {"status": "success", "action": "type_human", "length": len(text)}
