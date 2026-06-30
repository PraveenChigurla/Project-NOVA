"""
Interaction Strategy Engine.
Determines the optimal method to interact with a UI and handles fallbacks automatically.
"""
import logging
from typing import List

from nova.intelligence.interaction.strategy.models import InteractionIntent, InteractionTelemetry, StrategyResult
from nova.intelligence.interaction.strategy.strategies.base import InteractionStrategy

logger = logging.getLogger(__name__)

class InteractionStrategyEngine:
    """Orchestrates strategies in a prioritized fallback chain."""
    
    def __init__(self, strategies: List[InteractionStrategy] = None):
        # The order of this list is the fallback hierarchy
        self.strategies = strategies or []
        
    async def execute(self, intent: InteractionIntent, context: dict = None) -> InteractionTelemetry:
        """
        Attempts to fulfill the intent using the highest semantic strategy available.
        Automatically falls back to lower strategies if the higher ones fail.
        """
        logger.info(f"Strategy Engine routing intent: [{intent.action}] on '{intent.target}'")
        
        telemetry = InteractionTelemetry(intent=intent, success=False)
        
        for strategy in self.strategies:
            logger.debug(f"Attempting strategy: {strategy.strategy_type.value}")
            result = await strategy.execute(intent, context)
            
            telemetry.total_latency_ms += result.latency_ms
            telemetry.attempted_strategies.append(result)
            
            if result.success:
                logger.info(f"✅ Success using {strategy.strategy_type.value} strategy.")
                telemetry.success = True
                telemetry.final_strategy = strategy.strategy_type
                break
            else:
                logger.warning(f"❌ Strategy {strategy.strategy_type.value} failed: {result.error}")
                telemetry.fallback_count += 1
                
        if not telemetry.success:
            logger.error("All available interaction strategies failed.")
            
        return telemetry
