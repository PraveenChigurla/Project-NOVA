"""
Interaction Strategy Models.
Defines intents, strategies, and telemetry for the Universal UI Capability.
"""
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from enum import Enum
import time

class InteractionStrategyType(str, Enum):
    DOM = "dom"
    NATIVE_UI = "native_ui"
    VISION = "vision"
    PIXEL = "pixel"

class InteractionIntent(BaseModel):
    """A semantic request to interact with a UI element."""
    action: str = Field(..., description="e.g., 'click', 'type', 'read', 'wait'")
    target: str = Field(..., description="Semantic description, text, or selector of the target.")
    parameters: Dict[str, Any] = Field(default_factory=dict)
    
class StrategyResult(BaseModel):
    """The result of executing a specific strategy."""
    success: bool
    strategy_used: InteractionStrategyType
    data: Optional[Any] = None
    error: Optional[str] = None
    latency_ms: float = 0.0

class InteractionTelemetry(BaseModel):
    """Metrics gathered across the entire fallback loop."""
    intent: InteractionIntent
    success: bool
    final_strategy: Optional[InteractionStrategyType] = None
    fallback_count: int = 0
    attempted_strategies: List[StrategyResult] = Field(default_factory=list)
    total_latency_ms: float = 0.0
