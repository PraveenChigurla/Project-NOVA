"""
DOM Strategy.
Attempts to execute the interaction via the Web Automation Provider.
"""
import logging
from nova.intelligence.interaction.strategy.strategies.base import InteractionStrategy
from nova.intelligence.interaction.strategy.models import InteractionIntent, InteractionStrategyType
from nova.providers.base import ProviderRequest

logger = logging.getLogger(__name__)

class DOMStrategy(InteractionStrategy):
    
    def __init__(self, browser_provider):
        self.provider = browser_provider
        
    @property
    def strategy_type(self) -> InteractionStrategyType:
        return InteractionStrategyType.DOM
        
    async def _execute_internal(self, intent: InteractionIntent, context: dict = None) -> tuple[bool, any, str]:
        if not self.provider:
            return False, None, "WebAutomationProvider not available."
            
        try:
            # Map Universal UI Intents to Browser Provider Actions
            if intent.action == "click":
                req = ProviderRequest(action="click", payload={"selector": intent.target})
                res = await self.provider.execute(req)
                return res.get("success", False), res.get("data"), res.get("error", "Unknown Provider Error")
                
            elif intent.action == "type":
                # We need to fill the element with text
                text = intent.parameters.get("text", "")
                req = ProviderRequest(action="fill", payload={"selector": intent.target, "value": text})
                res = await self.provider.execute(req)
                return res.get("success", False), res.get("data"), res.get("error", "Unknown Provider Error")
                
            elif intent.action == "read_title":
                req = ProviderRequest(action="get_title", payload={})
                res = await self.provider.execute(req)
                return res.get("success", False), res.get("data"), res.get("error", "Unknown Provider Error")
                
            else:
                return False, None, f"DOM Strategy does not support action: {intent.action}"
                
        except Exception as e:
            return False, None, f"Provider Exception: {str(e)}"
