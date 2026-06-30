"""
Cognitive Layer Models.
Defines the structures that enrich a raw intent with real-world context before planning.
"""
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import datetime

class Goal(BaseModel):
    """The normalized objective."""
    id: str = Field(..., description="A canonical identifier for the goal (e.g., 'prepare_workspace')")
    raw_intent: str = Field(..., description="The original natural language input.")
    parameters: Dict[str, Any] = Field(default_factory=dict)

class ContextSnapshot(BaseModel):
    """Temporal and environmental context."""
    timestamp: float
    iso_date: str
    day_of_week: str
    hour: int
    timezone: str

class WorldState(BaseModel):
    """The physical state of the host operating system."""
    active_processes: List[str] = Field(default_factory=list, description="List of running process names (lowercase)")
    active_monitors: int = 1
    # Future: battery_percentage, network_status, active_browser_tabs
    
    def is_process_running(self, process_name: str) -> bool:
        return any(process_name.lower() in p for p in self.active_processes)

class ConstraintReport(BaseModel):
    """Rules and limits applied to this specific goal in this specific context."""
    ask_user_confirmation: bool = False
    skip_heavy_apps: bool = False
    reasons: List[str] = Field(default_factory=list)

from nova.intelligence.world.models import WorldGraph
from nova.intelligence.memory.models import MemorySnapshot

class CognitivePackage(BaseModel):
    """The fully enriched bundle handed to the Planner."""
    goal: Goal
    context: ContextSnapshot
    world: WorldGraph
    constraints: ConstraintReport
    memory: Optional[MemorySnapshot] = None

