"""
Planner Framework Models.
Defines the strict schema for Execution Plans and Steps.
"""

from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid

def _generate_id() -> str:
    return str(uuid.uuid4())

def _now() -> datetime:
    return datetime.now(timezone.utc)

class ExecutionStrategy(str, Enum):
    """How the plan should be executed."""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"

class RetryPolicy(BaseModel):
    """Defines how a failed step should be retried."""
    max_retries: int = Field(default=0)
    backoff_ms: int = Field(default=1000)
    
    class Config:
        frozen = True

class RollbackPolicy(BaseModel):
    """Defines what to do if a step fails definitively."""
    capability_id: str = Field(...)
    action: str = Field(...)
    parameters: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        frozen = True

class PlanStep(BaseModel):
    """A fundamental unit of work within an Execution Plan."""
    step_id: str = Field(default_factory=_generate_id)
    capability_id: str = Field(..., description="The capability responsible for executing this step")
    action: str = Field(..., description="The action to perform")
    parameters: Dict[str, Any] = Field(default_factory=dict)
    
    # DAG Relationships
    dependencies: List[str] = Field(default_factory=list, description="List of step_ids that must complete before this step")
    
    # Execution Metadata
    timeout_ms: int = Field(default=30000)
    retry_policy: RetryPolicy = Field(default_factory=RetryPolicy)
    rollback_policy: Optional[RollbackPolicy] = Field(None)
    human_approval_required: bool = Field(default=False)
    
    class Config:
        frozen = True

class ExecutionPlan(BaseModel):
    """The final compiled DAG of execution steps."""
    plan_id: str = Field(default_factory=_generate_id)
    intent: str = Field(...)
    strategy: ExecutionStrategy = Field(default=ExecutionStrategy.SEQUENTIAL)
    steps: List[PlanStep] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=_now)
    
    class Config:
        frozen = True

class PlannerContext(BaseModel):
    """Context window data passed into the planner."""
    session_id: str = Field(default_factory=_generate_id)
    history: List[Dict[str, Any]] = Field(default_factory=list)
    environment_state: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        frozen = True

class PlannerResult(BaseModel):
    """The outcome of a planning request."""
    success: bool = Field(...)
    plan: Optional[ExecutionPlan] = Field(None)
    error_message: Optional[str] = Field(None)
    elapsed_ms: float = Field(...)
    
    class Config:
        frozen = True
