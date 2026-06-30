"""
Project NOVA - Intent Framework Demonstration.
Demonstrates the 'Front Door' Pipeline: Raw Text -> Intent Parser -> Planner -> ExecutionPlan.
"""

import asyncio
import logging
import sys

from nova.intelligence.intents.models import Intent, IntentAlias
from nova.intelligence.intents.registry import IntentRegistry
from nova.intelligence.intents.parser import RuleIntentParser
from nova.intelligence.planning.planner import RuleBasedPlanner

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("nova.demo_intents")

async def main():
    logger.info("Initializing NOVA Intelligence Pipeline Demo...")
    
    # 1. Setup Intent Registry
    intent_registry = IntentRegistry()
    
    # Register the 'launch process' intent with some regex aliases
    launch_intent = Intent(
        name="desktop.process.launch",
        description="Launches a desktop application.",
        required_entities=["application"],
        aliases=[
            # Match "Open <app>", "Launch <app>", "Start <app>"
            IntentAlias(
                pattern=r"(?:open|launch|start|run)\s+([a-zA-Z0-9_\-\.]+)",
                entities_map={1: "application"}
            ),
            # Match "Can you please launch <app> for me"
            IntentAlias(
                pattern=r"(?:can you please)?\s*(?:open|launch|start|run)\s+([a-zA-Z0-9_\-\.]+)\s*(?:for me)?",
                entities_map={1: "application"}
            )
        ]
    )
    
    intent_registry.register(launch_intent)
    
    # 2. Setup Parser and Planner
    parser = RuleIntentParser(intent_registry)
    planner = RuleBasedPlanner()
    
    # -----------------------------------------------------------------
    # Test Cases
    # -----------------------------------------------------------------
    test_inputs = [
        "Open Notepad",
        "Can you please launch chrome for me?",
        "Start firefox.exe",
        "Make me a sandwich" # Unknown intent
    ]
    
    for raw_input in test_inputs:
        logger.info("\n" + "="*60)
        logger.info(f"USER INPUT: '{raw_input}'")
        logger.info("="*60)
        
        # Step 1: Parsing
        logger.info("-> 1. Intent Parser Running...")
        intent_result = await parser.parse(raw_input)
        
        logger.info(f"   [Normalized Intent]: {intent_result.intent_name}")
        logger.info(f"   [Extracted Entities]: {intent_result.entities}")
        logger.info(f"   [Confidence]: {intent_result.confidence}")
        
        if not intent_result.is_valid or intent_result.intent_name == "unknown":
            logger.warning("   [Status]: Failed to parse a valid intent. Stopping pipeline.")
            continue
            
        # Step 2: Planning
        logger.info("-> 2. Planner Running...")
        planner_result = await planner.plan(intent_result)
        
        if planner_result.success and planner_result.plan:
            logger.info("   [Status]: Plan Successfully Generated!")
            for idx, step in enumerate(planner_result.plan.steps):
                logger.info(f"   [Step {idx+1}]: {step.capability_id} -> {step.action} (Params: {step.parameters})")
        else:
            logger.error(f"   [Status]: Planner Failed - {planner_result.error_message}")
            
    logger.info("\nDemo complete. The Intelligence Pipeline successfully translates raw text into safe DAG plans.")

if __name__ == "__main__":
    asyncio.run(main())
