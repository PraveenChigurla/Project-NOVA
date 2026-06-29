"""
Cognitive Agent Runtime Models.
"""
from enum import Enum
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from nova.intelligence.llm.models import GoalContract

class AgentVote(str, Enum):
    ACCEPT = "accept"
    REJECT = "reject"
    ABSTAIN = "abstain"
    NEEDS_CONFIRMATION = "needs_confirmation"

class AgentContext(BaseModel):
    """The read-only state provided to an agent by the runtime."""
    goal: GoalContract
    world_summary: str
    memory_context: str

class AgentReasoning(BaseModel):
    """The output of an agent's reasoning process."""
    agent_id: str
    vote: AgentVote
    confidence: float
    rationale: str
    proposed_goal_refinements: Dict[str, Any] = Field(default_factory=dict)

class AgentConsensus(BaseModel):
    """The aggregated result of all agents reasoning about a goal."""
    original_goal: GoalContract
    final_decision: AgentVote
    reasonings: List[AgentReasoning]
    is_safe_to_plan: bool
    human_confirmation_required: bool
