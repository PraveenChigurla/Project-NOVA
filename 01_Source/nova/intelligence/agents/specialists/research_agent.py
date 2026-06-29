"""
Mock Research Agent.
Focuses on gathering context.
"""
from nova.intelligence.agents.interfaces import IAgent
from nova.intelligence.agents.models import AgentContext, AgentReasoning, AgentVote
from nova.intelligence.llm.models import GoalContract

class ResearchAgent(IAgent):
    
    def metadata(self) -> dict:
        return {"id": "research_agent", "version": "1.0", "expertise": "Information Retrieval"}
        
    def supports_goal(self, goal: GoalContract) -> bool:
        keywords = ["review", "find", "search", "summarize"]
        return any(k in goal.target_state.lower() for k in keywords)
        
    def reason(self, context: AgentContext) -> AgentReasoning:
        return AgentReasoning(
            agent_id="research_agent",
            vote=AgentVote.ACCEPT,
            confidence=0.85,
            rationale="I can summarize the repository structure before the Coding agent acts on it."
        )
