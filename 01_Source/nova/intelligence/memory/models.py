"""
Memory Models.
Defines the distinct structures for the five cognitive memory layers.
"""
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import time

class Fact(BaseModel):
    """Semantic Memory: A persistent fact."""
    key: str
    value: Any
    confidence: float = 1.0

class Episode(BaseModel):
    """Episodic Memory: A historical execution record."""
    timestamp: float = Field(default_factory=time.time)
    goal_id: str
    success: bool
    summary: str

class Procedure(BaseModel):
    """Procedural Memory: A learned sequence or skill recommendation."""
    goal_id: str
    recommended_skill: str

class MemorySnapshot(BaseModel):
    """The unified cognitive structure retrieved from all memory stores."""
    working_variables: Dict[str, Any] = Field(default_factory=dict)
    relevant_facts: List[Fact] = Field(default_factory=list)
    recent_episodes: List[Episode] = Field(default_factory=list)
    recommended_procedures: List[Procedure] = Field(default_factory=list)
