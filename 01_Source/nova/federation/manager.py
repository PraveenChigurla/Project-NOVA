"""
Federation Manager.
The orchestration layer for a sovereign NOVA node to interact with the Federation.
"""
import uuid
import logging
from typing import List
from nova.intelligence.llm.models import GoalContract
from nova.federation.models import NodeIdentity, CapabilityAdvertisement, DelegationRequest, DelegationResponse
from nova.federation.registry import NodeRegistry
from nova.federation.router import GoalRouter

logger = logging.getLogger(__name__)

class FederationManager:
    """Manages all inbound and outbound Federation traffic."""
    
    def __init__(self, node_id: str, local_capabilities: List[str]):
        self.identity = NodeIdentity(node_id=node_id)
        self.local_capabilities = local_capabilities
        
        self.registry = NodeRegistry(self.identity)
        self.router = GoalRouter(local_capabilities, self.registry)
        
    def broadcast_capabilities(self) -> CapabilityAdvertisement:
        """Generates an advertisement to be sent over the network transport."""
        logger.debug(f"[{self.identity.node_id}] Broadcasting capabilities: {self.local_capabilities}")
        return CapabilityAdvertisement(
            node=self.identity,
            capabilities=self.local_capabilities
        )
        
    def receive_advertisement(self, ad: CapabilityAdvertisement):
        """Processes an inbound advertisement from the network transport."""
        self.registry.register_peer_advertisement(ad)
        
    def route_goal(self, goal: GoalContract) -> DelegationRequest | None:
        """
        Determines if a goal should be sent to a peer. 
        Returns a DelegationRequest if it should be delegated, None if it stays local.
        """
        target_node = self.router.determine_target_node(goal)
        if target_node:
            req = DelegationRequest(
                request_id=str(uuid.uuid4()),
                source_node=self.identity,
                target_node_id=target_node.node_id,
                goal=goal
            )
            logger.info(f"[{self.identity.node_id}] Initiating delegation of '{goal.goal_id}' to '{target_node.node_id}'")
            return req
        return None
        
    def receive_delegation(self, req: DelegationRequest) -> DelegationResponse:
        """Handles an incoming delegation request from a peer."""
        logger.info(f"[{self.identity.node_id}] Received incoming delegation '{req.request_id}' from '{req.source_node.node_id}'")
        
        # Here, the Trust Framework and Policy Engine would normally evaluate the request.
        # Then, if approved, it goes into the local GoalEngine.
        
        logger.info(f"[{self.identity.node_id}] Executing delegated goal locally...")
        
        # Mock successful execution
        return DelegationResponse(
            request_id=req.request_id,
            success=True,
            result_data={"status": "executed_on_remote_node"}
        )
