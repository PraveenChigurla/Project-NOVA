"""
Context Assembler.
Formats deterministic state into a structured payload for the LLM.
"""
from typing import List
from nova.intelligence.world.models import WorldGraph
from nova.intelligence.memory.models import MemorySnapshot
from nova.intelligence.llm.models import ContextPayload

class ContextAssembler:
    """Prepares the ContextPayload for the LLM Provider."""
    
    def assemble(self, intent: str, world_graph: WorldGraph, memory_snapshot: MemorySnapshot) -> ContextPayload:
        # Format World Graph summary
        app_names = [e.attributes.get("name", e.id) for e in world_graph.get_entities_by_type("Application")]
        world_summary = f"Active Applications: {', '.join(app_names) if app_names else 'None'}"
        
        # Format Memory summary
        memories: List[str] = []
        for fact in memory_snapshot.relevant_facts:
            memories.append(f"Fact: {fact.key} = {fact.value}")
        for ep in memory_snapshot.recent_episodes:
            memories.append(f"Recent Episode: {ep.summary} (Success: {ep.success})")
            
        return ContextPayload(
            intent=intent,
            relevant_memories=memories,
            world_state_summary=world_summary
        )
