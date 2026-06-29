"""
Federation Models.
"""
from typing import List, Optional, Any
from pydantic import BaseModel, Field
from nova.intelligence.llm.models import GoalContract

class NodeIdentity(BaseModel):
    """The identity of a sovereign NOVA node."""
    node_id: str
    environment_type: str = "desktop"
    public_key: str = "mock_key"

class CapabilityAdvertisement(BaseModel):
    """A broadcast of what a node is capable of doing."""
    node: NodeIdentity
    capabilities: List[str] = Field(default_factory=list)

class DelegationRequest(BaseModel):
    """A request to transfer a Goal to another sovereign node."""
    request_id: str
    source_node: NodeIdentity
    target_node_id: str
    goal: GoalContract
    
class DelegationResponse(BaseModel):
    """The result of a delegated goal."""
    request_id: str
    success: bool
    result_data: Any
    error_message: Optional[str] = None
