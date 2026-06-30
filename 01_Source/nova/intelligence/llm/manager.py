"""
LLM Manager.
The orchestration layer for integrating LLMs as Cognitive Advisors.
"""
import logging
from nova.intelligence.world.models import WorldGraph
from nova.intelligence.memory.models import MemorySnapshot
from nova.intelligence.llm.models import GoalContract

from nova.intelligence.llm.engines.assembler import ContextAssembler
from nova.intelligence.llm.engines.validator import GoalContractValidator
from nova.intelligence.llm.engines.router import ModelRouter

from nova.intelligence.input.models import NormalizedInput

logger = logging.getLogger(__name__)

class LLMManager:
    """Orchestrates the Context Assembler, Model Router, and Contract Validator."""
    
    def __init__(self, router: ModelRouter):
        self.router = router
        self.assembler = ContextAssembler()
        self.validator = GoalContractValidator()
        
    def interpret_intent(self, input_obj: NormalizedInput, world_graph: WorldGraph, memory_snapshot: MemorySnapshot) -> GoalContract:
        """Translates natural language into a deterministic GoalContract using the LLM."""
        logger.info(f"LLMManager interpreting input from '{input_obj.source}': '{input_obj.text}'")
        
        # 1. Assemble stateless context
        payload = self.assembler.assemble(input_obj.text, world_graph, memory_snapshot)
        logger.debug(f"Assembled Payload with {len(payload.relevant_memories)} memories.")
        
        # 2. Route to provider
        provider = self.router.get_provider()
        
        # 3. Generate raw contract
        raw_response = provider.generate_contract(payload)
        
        # 4. Validate and coerce
        contract = self.validator.validate(raw_response)
        
        logger.info(f"LLM successfully mapped intent to Goal: '{contract.goal_id}' (Confidence: {contract.confidence})")
        return contract
