"""
Tests for the Cognitive Agent Runtime (CAR).
"""
import pytest
from nova.intelligence.llm.models import GoalContract
from nova.intelligence.agents.dispatcher import AgentDispatcher
from nova.intelligence.agents.specialists.coding_agent import CodingAgent
from nova.intelligence.agents.specialists.security_agent import SecurityAgent
from nova.intelligence.agents.models import AgentVote

def test_dispatcher_consensus_is_unanimous():
    agents = [CodingAgent(), SecurityAgent()]
    dispatcher = AgentDispatcher(agents)
    
    goal = GoalContract(
        goal_id="test_1",
        target_state="Review the code",
        required_capabilities=[],
        requires_confirmation=False
    )
    
    consensus = dispatcher.dispatch(goal, "", "")
    assert consensus.final_decision == AgentVote.ACCEPT
    assert consensus.is_safe_to_plan == True
    assert len(consensus.reasonings) == 2

def test_dispatcher_handles_security_veto():
    agents = [CodingAgent(), SecurityAgent()]
    dispatcher = AgentDispatcher(agents)
    
    goal = GoalContract(
        goal_id="test_2",
        target_state="Delete the code",
        required_capabilities=[],
        requires_confirmation=False
    )
    
    consensus = dispatcher.dispatch(goal, "", "")
    
    # Coding agent accepts, Security agent rejects. Result should be REJECT.
    assert consensus.final_decision == AgentVote.REJECT
    assert consensus.is_safe_to_plan == False
    assert consensus.human_confirmation_required == True
