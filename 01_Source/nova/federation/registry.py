"""
Node Registry.
Maintains awareness of other sovereign nodes on the network.
"""
import logging
from typing import Dict, List, Optional
from nova.federation.models import CapabilityAdvertisement, NodeIdentity

logger = logging.getLogger(__name__)

class NodeRegistry:
    """Tracks trusted peer nodes and their capabilities."""
    
    def __init__(self, local_identity: NodeIdentity):
        self.local_identity = local_identity
        self._peers: Dict[str, CapabilityAdvertisement] = {}
        
    def register_peer_advertisement(self, ad: CapabilityAdvertisement):
        """Records or updates a peer node's capabilities."""
        if ad.node.node_id == self.local_identity.node_id:
            return
            
        logger.info(f"Registry [{self.local_identity.node_id}]: Received capability broadcast from '{ad.node.node_id}'")
        self._peers[ad.node.node_id] = ad
        
    def find_node_with_capability(self, capability: str) -> Optional[NodeIdentity]:
        """Finds a peer that possesses the requested capability."""
        for peer_id, ad in self._peers.items():
            if capability in ad.capabilities:
                return ad.node
        return None
        
    def get_all_peers(self) -> List[NodeIdentity]:
        return [ad.node for ad in self._peers.values()]
