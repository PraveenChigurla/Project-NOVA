"""
Project NOVA - Cognitive Federation Runtime Demonstration.
Simulates two sovereign nodes dynamically routing Goals based on advertised capabilities.
"""
import sys
import logging
from nova.intelligence.llm.models import GoalContract
from nova.federation.manager import FederationManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("nova.demo_federation")

class MockNetworkBus:
    """Simulates a P2P network transport for demonstration purposes."""
    def __init__(self):
        self.nodes = {}
        
    def register(self, node: FederationManager):
        self.nodes[node.identity.node_id] = node
        
    def broadcast_ad(self, sender_id: str, ad):
        for node_id, node in self.nodes.items():
            if node_id != sender_id:
                node.receive_advertisement(ad)
                
    def send_delegation(self, req):
        target = self.nodes.get(req.target_node_id)
        if target:
            return target.receive_delegation(req)
        raise RuntimeError("Network Error: Target unreachable.")

def main():
    logger.info("Initializing Cognitive Federation Runtime...\n")
    
    network = MockNetworkBus()
    
    # 1. Initialize Sovereign Nodes
    desktop = FederationManager(node_id="Desktop_Node", local_capabilities=["browser", "vscode", "microphone"])
    server = FederationManager(node_id="HomeServer_Node", local_capabilities=["docker", "gpu", "database"])
    
    network.register(desktop)
    network.register(server)
    
    # 2. Discovery Phase
    logger.info("--- FEDERATION DISCOVERY ---")
    desktop_ad = desktop.broadcast_capabilities()
    server_ad = server.broadcast_capabilities()
    
    network.broadcast_ad("Desktop_Node", desktop_ad)
    network.broadcast_ad("HomeServer_Node", server_ad)
    
    # 3. Local Execution Scenario
    logger.info("\n--- SCENARIO 1: LOCAL EXECUTION ---")
    local_goal = GoalContract(
        goal_id="goal_1",
        target_state="Open VS Code",
        required_capabilities=["vscode"],
        requires_confirmation=False
    )
    
    delegation_req = desktop.route_goal(local_goal)
    if not delegation_req:
        logger.info("Desktop executes the Goal locally because it has 'vscode' capability.")
        
    # 4. Delegated Execution Scenario
    logger.info("\n--- SCENARIO 2: DELEGATED EXECUTION ---")
    gpu_goal = GoalContract(
        goal_id="goal_2",
        target_state="Train OCR Model",
        required_capabilities=["gpu"],
        requires_confirmation=False
    )
    
    delegation_req_2 = desktop.route_goal(gpu_goal)
    if delegation_req_2:
        logger.info(f"Desktop routing Goal over network transport to {delegation_req_2.target_node_id}...")
        response = network.send_delegation(delegation_req_2)
        logger.info(f"Desktop received response: {response.success} - {response.result_data}")
    
if __name__ == "__main__":
    if sys.platform != 'win32':
        logger.error("This demonstration requires Windows.")
        sys.exit(1)
    main()
