"""
Project NOVA - Universal UI Capability Demonstration.
Proves that NOVA can automatically route UI interactions to the optimal backend, falling back to Vision if DOM fails.
"""

import asyncio
import logging
import sys
import os

from nova.core.config import NovaConfig
from nova.core.kernel import NovaKernel
from nova.providers.base import ProviderMetadata, ProviderType, ProviderRequest
from nova.providers.browser.provider import WebAutomationProvider
from nova.providers.browser.adapters.playwright_adapter import PlaywrightAdapter
from nova.capabilities.base import CapabilityMetadata, CapabilityType

from nova.intelligence.interaction.strategy.engine import InteractionStrategyEngine
from nova.intelligence.interaction.strategy.strategies.dom_strategy import DOMStrategy
from nova.intelligence.interaction.strategy.strategies.vision_strategy import VisionStrategy
from nova.capabilities.universal.ui_capability import UniversalUICapability
from nova.intelligence.planning.models import ExecutionPlan, PlanStep, ExecutionStrategy

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("nova.demo_universal_ui")

async def main():
    logger.info("Initializing NOVA Kernel...")
    config = NovaConfig()
    kernel = NovaKernel(config)
    await kernel.boot()
    
    # 1. Setup DOM Backend (Web Automation Provider)
    adapter = PlaywrightAdapter()
    browser_provider = WebAutomationProvider(
        metadata=ProviderMetadata(
            id="com.nova.provider.web_automation", 
            name="Web Automation", 
            version="1.0", 
            type=ProviderType.BROWSER
        ),
        adapter=adapter
    )
    kernel.provider_registry.register(browser_provider)
    await browser_provider.initialize()
    await browser_provider.start()
    
    # We must manually launch for the demo so we have a target
    await browser_provider.execute(ProviderRequest(action="launch", payload={"headless": False}))
    await browser_provider.execute(ProviderRequest(action="navigate", payload={"url": "https://example.com"}))
    
    # 2. Setup Strategies
    dom_strategy = DOMStrategy(browser_provider)
    vision_strategy = VisionStrategy(kernel)
    
    # The Engine is configured with a strict fallback hierarchy: DOM -> Vision
    strategy_engine = InteractionStrategyEngine(strategies=[dom_strategy, vision_strategy])
    
    # 3. Setup Universal UI Capability
    ui_cap = UniversalUICapability(
        metadata=CapabilityMetadata(
            id="com.nova.universal.ui",
            name="Universal UI",
            version="1.0.0",
            type=CapabilityType.EXECUTION
        ),
        strategy_engine=strategy_engine
    )
    ui_cap.kernel = kernel
    kernel.capability_registry.register(ui_cap)
    
    logger.info("\n>>> SCENARIO A: DOM SUCCESS <<<")
    # This element exists in the DOM
    plan_a = ExecutionPlan(
        intent="Read Title",
        strategy=ExecutionStrategy.SEQUENTIAL,
        steps=[
            PlanStep(
                step_id="step_a",
                capability_id="com.nova.universal.ui",
                action="ui_read",
                parameters={"target": "page_title"}
            )
        ]
    )
    res_a = await kernel.execution_engine.execute_plan(plan_a)
    logger.info(f"Result A: {res_a.data}")
    
    logger.info("\n>>> SCENARIO B: DOM FAILURE -> VISION FALLBACK <<<")
    # This element does not exist in the DOM (simulating a canvas app or a desktop app)
    plan_b = ExecutionPlan(
        intent="Click Canvas Button",
        strategy=ExecutionStrategy.SEQUENTIAL,
        steps=[
            PlanStep(
                step_id="step_b",
                capability_id="com.nova.universal.ui",
                action="ui_click",
                parameters={"target": "Hidden Canvas Button"}
            )
        ]
    )
    res_b = await kernel.execution_engine.execute_plan(plan_b)
    logger.info(f"Result B: {res_b.data}")
    
    logger.info("\nCleaning up...")
    await asyncio.sleep(2.0)
    await browser_provider.stop()
    await kernel.shutdown()
    logger.info("Demonstration Complete.")

if __name__ == "__main__":
    if sys.platform != 'win32':
        logger.error("This demonstration requires Windows.")
        sys.exit(1)
    asyncio.run(main())
