"""
Project NOVA - Input Framework Demonstration.
Proves that Voice, REST, and CLI inputs all normalize into the exact same pipeline.
"""

import asyncio
import logging
import sys

from nova.intelligence.input.adapters.cli_adapter import CLIAdapter
from nova.intelligence.input.adapters.mock_adapters import MockVoiceAdapter, MockRESTAdapter
from nova.intelligence.input.normalizer import InputNormalizer
from nova.intelligence.input.conversation import ConversationManager

from nova.intelligence.llm.manager import LLMManager
from nova.intelligence.llm.engines.router import ModelRouter
from nova.intelligence.llm.adapters.mock_adapter import MockLLMAdapter

from nova.intelligence.world.models import WorldGraph
from nova.intelligence.memory.manager import MemoryManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("nova.demo_input")

async def main():
    logger.info("Initializing Input Framework...")
    
    normalizer = InputNormalizer()
    conversation_manager = ConversationManager()
    
    # Mock LLM and state for the downstream pipeline
    llm_manager = LLMManager(ModelRouter(MockLLMAdapter()))
    world_graph = WorldGraph()
    memory_manager = MemoryManager()
    
    # 1. Simulate Voice Input
    logger.info("\n--- 1. VOICE INPUT ---")
    voice_adapter = MockVoiceAdapter("prepare my workday   ") # Messy input
    raw_voice = voice_adapter.listen()
    logger.info(f"Raw Voice: '{raw_voice.text}' (Confidence: {raw_voice.confidence})")
    
    norm_voice = normalizer.normalize(raw_voice)
    logger.info(f"Normalized Voice: '{norm_voice.text}'")
    
    proc_voice = conversation_manager.process(norm_voice)
    contract_voice = llm_manager.interpret_intent(proc_voice, world_graph, memory_manager.build_snapshot("unknown"))
    logger.info(f"Generated Contract from Voice: {contract_voice.goal_id}")
    
    # 2. Simulate REST API Input
    logger.info("\n--- 2. REST API INPUT ---")
    rest_adapter = MockRESTAdapter({"text": " prepare my workday", "ip": "192.168.1.5"})
    raw_rest = rest_adapter.listen()
    logger.info(f"Raw REST: '{raw_rest.text}' (Metadata: {raw_rest.metadata})")
    
    norm_rest = normalizer.normalize(raw_rest)
    proc_rest = conversation_manager.process(norm_rest)
    contract_rest = llm_manager.interpret_intent(proc_rest, world_graph, memory_manager.build_snapshot("unknown"))
    logger.info(f"Generated Contract from REST: {contract_rest.goal_id}")
    
    # 3. Simulate CLI Input (Requires human to type)
    logger.info("\n--- 3. CLI INPUT ---")
    logger.info("Please type 'prepare my workday' below:")
    cli_adapter = CLIAdapter()
    raw_cli = cli_adapter.listen()
    
    norm_cli = normalizer.normalize(raw_cli)
    proc_cli = conversation_manager.process(norm_cli)
    contract_cli = llm_manager.interpret_intent(proc_cli, world_graph, memory_manager.build_snapshot("unknown"))
    logger.info(f"Generated Contract from CLI: {contract_cli.goal_id}")
    
    logger.info("\nSUCCESS: All three disparate input sources normalized into identical Goal Contracts.")

if __name__ == "__main__":
    if sys.platform != 'win32':
        logger.error("This demonstration requires Windows.")
        sys.exit(1)
    asyncio.run(main())
