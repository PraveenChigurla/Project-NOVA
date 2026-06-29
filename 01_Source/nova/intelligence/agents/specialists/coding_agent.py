"""
Mock Coding Agent.
Focuses on software architecture and logic.
"""
from nova.intelligence.agents.interfaces import IAgent
from nova.intelligence.agents.models import AgentContext, AgentReasoning, AgentVote
from nova.intelligence.llm.models import GoalContract

class CodingAgent(IAgent):
    
    def metadata(self) -> dict:
        return {"id": "coding_agent", "version": "1.0", "expertise": "Software Engineering"}
        
    def supports_goal(self, goal: GoalContract) -> bool:
        keywords = ["code", "repository", "delete", "refactor", "review"]
        return any(k in goal.target_state.lower() for k in keywords)
        
    def reason(self, context: AgentContext) -> AgentReasoning:
        # Mock logic
        if "delete 5,000 files" in context.goal.target_state.lower():
            return AgentReasoning(
                agent_id="coding_agent",
                vote=AgentVote.ACCEPT,
                confidence=0.8,
                rationale="Scripting a mass deletion is a trivial coding task. I can write the logic."
            )
            
        return AgentReasoning(
            agent_id="coding_agent",
            vote=AgentVote.ACCEPT,
            confidence=0.9,
            rationale="I can review the repository architecture and suggest improvements."
        )
