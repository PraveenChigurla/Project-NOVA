"""
LLM Data Models.
Defines the strict contracts bounding the LLM's output.
"""
from typing import Dict, Any, List
from pydantic import BaseModel, Field

class GoalContract(BaseModel):
    """The structured output required from the LLM. It maps natural language to a deterministic Goal."""
    goal_id: str = Field(..., description="The canonical ID of the goal (e.g., 'prepare_workspace')")
    confidence: float = Field(..., description="The LLM's confidence in this translation (0.0 to 1.0)")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Extracted parameters")
    requires_confirmation: bool = Field(default=False, description="Whether the LLM thinks this is destructive/ambiguous")
    reasoning_summary: str = Field(..., description="A brief explanation of why this goal was chosen")
    safety_flags: List[str] = Field(default_factory=list, description="Any detected risks (e.g., 'Modifies filesystem')")

class ContextPayload(BaseModel):
    """The assembled context passed to the LLM to help it reason."""
    intent: str = Field(..., description="The raw natural language input")
    relevant_memories: List[str] = Field(default_factory=list)
    world_state_summary: str = Field(..., description="A textual summary of the World Graph")
