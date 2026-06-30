"""
Mouse Capability.
Orchestrates human-like mouse interaction using the Interaction Engine and Mouse Provider.
"""
import asyncio
import logging
from typing import Dict, Any, Optional

from nova.capabilities.base import Capability, CapabilityMetadata, CapabilityType
from nova.security.permissions.models import PermissionScope
from nova.providers.base import ProviderRequest
from nova.intelligence.interaction.engine import InteractionEngine, MovementProfile

logger = logging.getLogger(__name__)

class MouseCapability(Capability):
    """Execution bridge mapping Planner intents to human-like Mouse movements."""
    
    def __init__(self, metadata: CapabilityMetadata):
        super().__init__(metadata)
        self.interaction_engine = InteractionEngine()
        
    async def initialize(self) -> None:
        logger.info(f"[{self.metadata.id}] Initializing Mouse Capability...")
        
    async def execute(self, action: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes a semantic mouse action.
        Supports: 'move_human', 'click_human'
        """
        if not self.kernel:
            raise RuntimeError("MouseCapability requires Kernel attachment.")
            
        provider = self.kernel.provider_registry.get("com.nova.provider.mouse")
        if not provider:
            raise RuntimeError("Required provider 'com.nova.provider.mouse' not found.")
            
        logger.debug(f"[{self.metadata.id}] Executing semantic action: {action}")
        
        if action == "move_human":
            # 1. Permission Check
            await self.kernel.permission_manager.request(
                self.metadata.id, PermissionScope.OS_MOUSE_MOVE, f"Move mouse to {parameters}"
            )
            
            return await self._execute_human_move(provider, parameters)
            
        elif action == "click_human":
            # 1. Move humanly to the target first (if coordinates provided)
            # 2. Fire the click
            await self.kernel.permission_manager.request(
                self.metadata.id, PermissionScope.OS_MOUSE_CLICK, f"Click mouse at {parameters}"
            )
            
            if "x" in parameters and "y" in parameters:
                await self._execute_human_move(provider, parameters)
                
            # Simulate Hover Delay
            await asyncio.sleep(self.interaction_engine.config.hover_delay_ms / 1000.0)
            
            req = ProviderRequest(action="click", payload={"button": parameters.get("button", "left")})
            await provider.execute(req)
            
            return {"status": "success", "action": "click_human"}
            
        raise ValueError(f"Unknown action: {action}")
        
    async def _execute_human_move(self, provider, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Generates a Bezier stream and iteratively dispatches it to the Native Provider."""
        target_x = parameters["x"]
        target_y = parameters["y"]
        profile_str = parameters.get("profile", "natural")
        
        try:
            profile = MovementProfile(profile_str)
        except ValueError:
            profile = MovementProfile.NATURAL
            
        # Get starting position natively
        pos_req = ProviderRequest(action="get_position", payload={})
        pos_res = await provider.execute(pos_req)
        start_x, start_y = pos_res["x"], pos_res["y"]
        
        # Generate mathematical curve
        stream = self.interaction_engine.generate_movement_stream(start_x, start_y, target_x, target_y, profile)
        
        logger.info(f"[{self.metadata.id}] Dispatched {profile.value} movement stream with {len(stream)} bezier steps.")
        
        # Execute the stream natively
        for x, y, delay_sec in stream:
            req = ProviderRequest(action="move_cursor", payload={"x": x, "y": y})
            await provider.execute(req)
            if delay_sec > 0:
                await asyncio.sleep(delay_sec)
                
        return {"status": "success", "action": "move_human", "final_x": target_x, "final_y": target_y}
