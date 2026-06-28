"""
Execution Engine Models.
Defines the runtime execution states and results.
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

class SessionState(str, Enum):
    """The state of an execution session."""
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLING_BACK = "rolling_back"
    ROLLED_BACK = "rolled_back"

class StepResult(BaseModel):
    """The outcome of an individual PlanStep."""
    step_id: str = Field(...)
    capability_id: str = Field(...)
    action: str = Field(...)
    success: bool = Field(...)
    data: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = Field(None)
    retries_used: int = Field(default=0)
    elapsed_ms: float = Field(...)
    timestamp: datetime = Field(default_factory=_now)
    rolled_back: bool = Field(default=False)

    class Config:
        frozen = False # Mutated during rollback

class ExecutionContext(BaseModel):
    """Context and variables shared across steps in a session."""
    variables: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        frozen = False # Mutated by steps during execution

class ExecutionResult(BaseModel):
    """The final outcome of an ExecutionPlan."""
    plan_id: str = Field(...)
    session_id: str = Field(...)
    success: bool = Field(...)
    state: SessionState = Field(...)
    step_results: List[StepResult] = Field(default_factory=list)
    error_message: Optional[str] = Field(None)
    total_elapsed_ms: float = Field(...)
    
    class Config:
        frozen = True

class ExecutionSession(BaseModel):
    """The active state of an executing plan."""
    session_id: str = Field(default_factory=_generate_id)
    plan_id: str = Field(...)
    state: SessionState = Field(default=SessionState.PENDING)
    context: ExecutionContext = Field(default_factory=ExecutionContext)
    step_results: Dict[str, StepResult] = Field(default_factory=dict)
    start_time: datetime = Field(default_factory=_now)
    
    class Config:
        frozen = False
