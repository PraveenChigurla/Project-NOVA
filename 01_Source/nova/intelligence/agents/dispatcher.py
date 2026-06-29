"""
Agent Dispatcher.
Selects appropriate agents, aggregates their reasoning, and handles Consensus Voting.
"""
import logging
from typing import List
from nova.intelligence.agents.interfaces import IAgent
from nova.intelligence.agents.models import AgentContext, AgentConsensus, AgentVote
from nova.intelligence.llm.models import GoalContract

logger = logging.getLogger(__name__)

class AgentDispatcher:
    """Manages the Cognitive Agent Runtime."""
    
    def __init__(self, registered_agents: List[IAgent]):
        self.agents = registered_agents
        
    def dispatch(self, goal: GoalContract, world_summary: str, memory_context: str) -> AgentConsensus:
        """Invokes relevant agents and aggregates consensus."""
        logger.info(f"AgentDispatcher processing Goal: '{goal.target_state}'")
        
        context = AgentContext(
            goal=goal,
            world_summary=world_summary,
            memory_context=memory_context
        )
        
        # 1. Selection
        active_agents = [a for a in self.agents if a.supports_goal(goal)]
        logger.info(f"Selected {len(active_agents)} agents for consultation.")
        
        if not active_agents:
            # If no agent cares, the runtime proceeds normally.
            return AgentConsensus(
                original_goal=goal,
                final_decision=AgentVote.ACCEPT,
                reasonings=[],
                is_safe_to_plan=True,
                human_confirmation_required=False
            )
            
        # 2. Reasoning
        reasonings = []
        for agent in active_agents:
            logger.debug(f"Invoking {agent.metadata()['id']}...")
            reasoning = agent.reason(context)
            reasonings.append(reasoning)
            
        # 3. Consensus & Conflict Resolution
        return self._evaluate_consensus(goal, reasonings)
        
    def _evaluate_consensus(self, goal: GoalContract, reasonings: list) -> AgentConsensus:
        """Determines final decision based on agent votes."""
        final_vote = AgentVote.ACCEPT
        is_safe = True
        needs_human = False
        
        for r in reasonings:
            logger.info(f"Vote from {r.agent_id}: {r.vote.value.upper()} (Confidence: {r.confidence:.2f}) - {r.rationale}")
            if r.vote == AgentVote.REJECT:
                logger.warning(f"VETO TRIGGERED by {r.agent_id}!")
                final_vote = AgentVote.REJECT
                is_safe = False
                needs_human = True
                break # A single reject halts automatic execution
                
        return AgentConsensus(
            original_goal=goal,
            final_decision=final_vote,
            reasonings=reasonings,
            is_safe_to_plan=is_safe,
            human_confirmation_required=needs_human
        )
