"""
Universal UI Capability.
The unified entry point for all graphical UI interactions in NOVA.
"""
import logging
from typing import Dict, Any

from nova.capabilities.base import Capability, CapabilityMetadata, CapabilityType
from nova.intelligence.interaction.strategy.engine import InteractionStrategyEngine
from nova.intelligence.interaction.strategy.models import InteractionIntent

logger = logging.getLogger(__name__)

class UniversalUICapability(Capability):
    """
    Executes UI goals without worrying about the underlying automation technology.
    """
    
    def __init__(self, metadata: CapabilityMetadata, strategy_engine: InteractionStrategyEngine):
        super().__init__(metadata)
        self.strategy_engine = strategy_engine
        
    async def initialize(self) -> None:
        logger.info(f"[{self.metadata.id}] Initializing Universal UI Capability...")
        
    async def execute(self, action: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes a semantic UI action.
        Supports: 'ui_click', 'ui_type', 'ui_read'
        """
        logger.debug(f"[{self.metadata.id}] Executing action: {action}")
        
        target = parameters.get("target")
        if not target:
            raise ValueError("All UI actions require a 'target' parameter.")
            
        # Map generic execution actions to Strategy Intents
        if action == "ui_click":
            intent = InteractionIntent(action="click", target=target, parameters=parameters)
        elif action == "ui_type":
            intent = InteractionIntent(action="type", target=target, parameters=parameters)
        elif action == "ui_read":
            intent = InteractionIntent(action="read_title", target=target, parameters=parameters)
        else:
            raise ValueError(f"Unknown action: {action}")
            
        # Let the Strategy Engine figure out HOW to execute it
        telemetry = await self.strategy_engine.execute(intent)
        
        return {
            "status": "success" if telemetry.success else "failed",
            "action": action,
            "target": target,
            "strategy_used": telemetry.final_strategy.value if telemetry.final_strategy else "none",
            "fallback_count": telemetry.fallback_count,
            "latency_ms": telemetry.total_latency_ms
        }
