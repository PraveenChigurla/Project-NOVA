"""
Mock Security Agent.
Extremely conservative. Vetoes destructive goals.
"""
from nova.intelligence.agents.interfaces import IAgent
from nova.intelligence.agents.models import AgentContext, AgentReasoning, AgentVote
from nova.intelligence.llm.models import GoalContract

class SecurityAgent(IAgent):
    
    def metadata(self) -> dict:
        return {"id": "security_agent", "version": "1.0", "expertise": "Risk Mitigation"}
        
    def supports_goal(self, goal: GoalContract) -> bool:
        # Security agent cares about everything that modifies state.
        return True
        
    def reason(self, context: AgentContext) -> AgentReasoning:
        # Mock logic
        if "delete" in context.goal.target_state.lower():
            return AgentReasoning(
                agent_id="security_agent",
                vote=AgentVote.REJECT,
                confidence=0.99,
                rationale="Mass file deletion is a high-risk operation that violates zero-trust policies."
            )
            
        return AgentReasoning(
            agent_id="security_agent",
            vote=AgentVote.ACCEPT,
            confidence=0.7,
            rationale="Goal appears non-destructive. Proceed with caution."
        )
