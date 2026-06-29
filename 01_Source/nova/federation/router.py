"""
Goal Router.
Decides whether a Goal should be executed locally or delegated to a peer.
"""
import logging
from typing import Optional, List
from nova.intelligence.llm.models import GoalContract
from nova.federation.models import NodeIdentity
from nova.federation.registry import NodeRegistry

logger = logging.getLogger(__name__)

class GoalRouter:
    """Routes goals based on local vs remote capabilities."""
    
    def __init__(self, local_capabilities: List[str], registry: NodeRegistry):
        self.local_capabilities = local_capabilities
        self.registry = registry
        
    def determine_target_node(self, goal: GoalContract) -> Optional[NodeIdentity]:
        """Returns None if the goal can be handled locally, or a NodeIdentity if it should be delegated."""
        # Simple heuristic: If the goal explicitly requires a capability we don't have.
        for req_cap in goal.required_capabilities:
            if req_cap not in self.local_capabilities:
                logger.info(f"GoalRouter: Local node lacks required capability '{req_cap}'. Searching Federation...")
                
                # We need to delegate.
                target_node = self.registry.find_node_with_capability(req_cap)
                if target_node:
                    logger.info(f"GoalRouter: Found target node '{target_node.node_id}' with capability '{req_cap}'.")
                    return target_node
                else:
                    logger.error(f"GoalRouter: NO FEDERATED NODE found with capability '{req_cap}'. Goal cannot be executed.")
                    raise RuntimeError(f"Capability '{req_cap}' not found in Federation.")
                    
        # If we have all required capabilities, run it locally.
        logger.info(f"GoalRouter: Local node can satisfy all capabilities. Retaining goal.")
        return None
