"""
Memory Manager.
The central coordinator for NOVA's cognitive memory architecture.
"""
import logging
from nova.intelligence.memory.interfaces import (
    WorkingMemoryInterface, EpisodicMemoryInterface, 
    SemanticMemoryInterface, ProceduralMemoryInterface
)
from nova.intelligence.memory.stores.ephemeral import (
    EphemeralWorkingMemory, EphemeralEpisodicMemory, 
    EphemeralSemanticMemory, EphemeralProceduralMemory
)
from nova.intelligence.memory.models import MemorySnapshot

logger = logging.getLogger(__name__)

class MemoryManager:
    """Routes queries to the appropriate specialized cognitive memory layer."""
    
    def __init__(self):
        # Defaulting to ephemeral stores for Sprint 20.
        self.working = EphemeralWorkingMemory()
        self.episodic = EphemeralEpisodicMemory()
        self.semantic = EphemeralSemanticMemory()
        self.procedural = EphemeralProceduralMemory()
        
    def initialize_session(self):
        """Prepares memory for a new execution session (clears working memory)."""
        logger.debug("Initializing new execution session. Clearing Working Memory.")
        self.working.clear()
        
    def build_snapshot(self, current_goal_id: str) -> MemorySnapshot:
        """Constructs a unified cognitive memory package for the Planner."""
        logger.info(f"Building MemorySnapshot for Goal: '{current_goal_id}'")
        
        # Pull facts (In a real DB, we'd query by relevance or embeddings)
        # For now, we'll just grab the whole dictionary of facts for context.
        facts = list(self.semantic._facts.values()) 
        
        # Pull recent episodes
        episodes = self.episodic.retrieve_recent(limit=3)
        
        # Pull procedures specific to this goal
        procedures = self.procedural.get_procedures(current_goal_id)
        
        snapshot = MemorySnapshot(
            working_variables=self.working.get_all(),
            relevant_facts=facts,
            recent_episodes=episodes,
            recommended_procedures=procedures
        )
        
        logger.debug(f"Memory Snapshot Built: {len(facts)} facts, {len(episodes)} episodes.")
        return snapshot
