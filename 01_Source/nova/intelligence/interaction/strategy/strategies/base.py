"""
Strategy Base Interface.
"""
from abc import ABC, abstractmethod
import time
from nova.intelligence.interaction.strategy.models import InteractionIntent, StrategyResult, InteractionStrategyType

class InteractionStrategy(ABC):
    """Abstract base class for all execution strategies."""
    
    @property
    @abstractmethod
    def strategy_type(self) -> InteractionStrategyType:
        pass
        
    async def execute(self, intent: InteractionIntent, context: dict = None) -> StrategyResult:
        """Executes the strategy and measures latency."""
        start_time = time.time()
        try:
            success, data, error = await self._execute_internal(intent, context)
            latency = (time.time() - start_time) * 1000
            return StrategyResult(
                success=success,
                strategy_used=self.strategy_type,
                data=data,
                error=error,
                latency_ms=latency
            )
        except Exception as e:
            latency = (time.time() - start_time) * 1000
            return StrategyResult(
                success=False,
                strategy_used=self.strategy_type,
                error=str(e),
                latency_ms=latency
            )
            
    @abstractmethod
    async def _execute_internal(self, intent: InteractionIntent, context: dict = None) -> tuple[bool, any, str]:
        """
        Internal implementation of the strategy.
        Returns: (success: bool, data: any, error: str)
        """
        pass
