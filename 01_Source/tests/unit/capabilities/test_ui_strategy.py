"""
Tests for the Universal UI Capability and Strategy Engine.
"""
import pytest
from nova.intelligence.interaction.strategy.engine import InteractionStrategyEngine
from nova.intelligence.interaction.strategy.strategies.base import InteractionStrategy
from nova.intelligence.interaction.strategy.models import InteractionIntent, InteractionStrategyType

class MockFailStrategy(InteractionStrategy):
    @property
    def strategy_type(self) -> InteractionStrategyType:
        return InteractionStrategyType.DOM
        
    async def _execute_internal(self, intent: InteractionIntent, context: dict = None) -> tuple[bool, any, str]:
        return False, None, "Mock DOM Failure"

class MockSuccessStrategy(InteractionStrategy):
    @property
    def strategy_type(self) -> InteractionStrategyType:
        return InteractionStrategyType.VISION
        
    async def _execute_internal(self, intent: InteractionIntent, context: dict = None) -> tuple[bool, any, str]:
        return True, {"mock": "data"}, None

@pytest.mark.asyncio
async def test_strategy_fallback_loop():
    s1 = MockFailStrategy()
    s2 = MockSuccessStrategy()
    
    engine = InteractionStrategyEngine(strategies=[s1, s2])
    
    intent = InteractionIntent(action="click", target="test")
    telemetry = await engine.execute(intent)
    
    assert telemetry.success == True
    assert telemetry.fallback_count == 1
    assert telemetry.final_strategy == InteractionStrategyType.VISION
    assert len(telemetry.attempted_strategies) == 2
    
    # First attempt should be DOM (failed)
    assert telemetry.attempted_strategies[0].strategy_used == InteractionStrategyType.DOM
    assert telemetry.attempted_strategies[0].success == False
    
    # Second attempt should be VISION (success)
    assert telemetry.attempted_strategies[1].strategy_used == InteractionStrategyType.VISION
    assert telemetry.attempted_strategies[1].success == True
