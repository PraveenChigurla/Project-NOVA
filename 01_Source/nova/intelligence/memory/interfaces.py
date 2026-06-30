"""
Memory Interfaces.
Abstract definitions for the five cognitive memory subsystems.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Any
from nova.intelligence.memory.models import Fact, Episode, Procedure

class WorkingMemoryInterface(ABC):
    @abstractmethod
    def set(self, key: str, value: Any) -> None: pass
    
    @abstractmethod
    def get(self, key: str) -> Optional[Any]: pass
    
    @abstractmethod
    def clear(self) -> None: pass
    
    @abstractmethod
    def get_all(self) -> dict: pass

class EpisodicMemoryInterface(ABC):
    @abstractmethod
    def record(self, episode: Episode) -> None: pass
    
    @abstractmethod
    def retrieve_recent(self, limit: int = 5) -> List[Episode]: pass

class SemanticMemoryInterface(ABC):
    @abstractmethod
    def store_fact(self, fact: Fact) -> None: pass
    
    @abstractmethod
    def get_fact(self, key: str) -> Optional[Fact]: pass

class ProceduralMemoryInterface(ABC):
    @abstractmethod
    def store_procedure(self, procedure: Procedure) -> None: pass
    
    @abstractmethod
    def get_procedures(self, goal_id: str) -> List[Procedure]: pass
