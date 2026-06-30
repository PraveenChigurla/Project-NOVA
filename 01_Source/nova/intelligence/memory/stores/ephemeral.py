"""
Ephemeral Memory Stores.
In-memory dictionary implementations of the Cognitive Memory layers.
"""
from typing import Dict, Any, List, Optional
from nova.intelligence.memory.interfaces import (
    WorkingMemoryInterface, 
    EpisodicMemoryInterface, 
    SemanticMemoryInterface, 
    ProceduralMemoryInterface
)
from nova.intelligence.memory.models import Fact, Episode, Procedure

class EphemeralWorkingMemory(WorkingMemoryInterface):
    def __init__(self):
        self._data: Dict[str, Any] = {}
        
    def set(self, key: str, value: Any) -> None:
        self._data[key] = value
        
    def get(self, key: str) -> Optional[Any]:
        return self._data.get(key)
        
    def clear(self) -> None:
        self._data.clear()
        
    def get_all(self) -> dict:
        return self._data.copy()


class EphemeralEpisodicMemory(EpisodicMemoryInterface):
    def __init__(self):
        self._episodes: List[Episode] = []
        
    def record(self, episode: Episode) -> None:
        self._episodes.append(episode)
        
    def retrieve_recent(self, limit: int = 5) -> List[Episode]:
        # Sort by timestamp descending
        sorted_eps = sorted(self._episodes, key=lambda e: e.timestamp, reverse=True)
        return sorted_eps[:limit]


class EphemeralSemanticMemory(SemanticMemoryInterface):
    def __init__(self):
        self._facts: Dict[str, Fact] = {}
        
    def store_fact(self, fact: Fact) -> None:
        self._facts[fact.key] = fact
        
    def get_fact(self, key: str) -> Optional[Fact]:
        return self._facts.get(key)


class EphemeralProceduralMemory(ProceduralMemoryInterface):
    def __init__(self):
        self._procedures: List[Procedure] = []
        
    def store_procedure(self, procedure: Procedure) -> None:
        self._procedures.append(procedure)
        
    def get_procedures(self, goal_id: str) -> List[Procedure]:
        return [p for p in self._procedures if p.goal_id == goal_id]
