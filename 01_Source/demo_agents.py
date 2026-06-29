"""
Project NOVA - Cognitive Agent Runtime Demonstration.
Simulates Multi-Agent consensus and conflict resolution over a Goal.
"""
import sys
import logging
from nova.intelligence.llm.models import GoalContract
from nova.intelligence.agents.dispatcher import AgentDispatcher
from nova.intelligence.agents.specialists.coding_agent import CodingAgent
from nova.intelligence.agents.specialists.security_agent import SecurityAgent
from nova.intelligence.agents.specialists.research_agent import ResearchAgent

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("nova.demo_agents")

def main():
    logger.info("Initializing Cognitive Agent Runtime...")
    
    # Register agents
    agents = [
        CodingAgent(),
        SecurityAgent(),
        ResearchAgent()
    ]
    dispatcher = AgentDispatcher(agents)
    
    # 1. Unanimous Scenario
    logger.info("\n--- SCENARIO 1: UNANIMOUS CONSENSUS ---")
    safe_goal = GoalContract(
        goal_id="goal_1",
        target_state="Review the repository and summarize architecture",
        required_capabilities=[],
        requires_confirmation=False
    )
    
    consensus_1 = dispatcher.dispatch(safe_goal, "Empty World", "Empty Memory")
    logger.info(f"Final Decision: {consensus_1.final_decision.value.upper()}")
    logger.info(f"Is Safe to Plan? {consensus_1.is_safe_to_plan}")
    
    
    # 2. Conflict Scenario
    logger.info("\n--- SCENARIO 2: MULTI-AGENT CONFLICT ---")
    unsafe_goal = GoalContract(
        goal_id="goal_2",
        target_state="Delete 5,000 files in the src directory",
        required_capabilities=[],
        requires_confirmation=False
    )
    
    consensus_2 = dispatcher.dispatch(unsafe_goal, "Empty World", "Empty Memory")
    logger.info(f"Final Decision: {consensus_2.final_decision.value.upper()}")
    logger.info(f"Is Safe to Plan? {consensus_2.is_safe_to_plan}")
    logger.warning(f"Needs Human Confirmation? {consensus_2.human_confirmation_required}")
    
if __name__ == "__main__":
    if sys.platform != 'win32':
        logger.error("This demonstration requires Windows.")
        sys.exit(1)
    main()
