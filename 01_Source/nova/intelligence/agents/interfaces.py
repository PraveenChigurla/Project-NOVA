"""
Agent Interfaces.
Defines the strict contract all agents must implement. Noticeably absent: execution.
"""
from abc import ABC, abstractmethod
from nova.intelligence.agents.models import AgentContext, AgentReasoning
from nova.intelligence.llm.models import GoalContract

class IAgent(ABC):
    """The base contract for a NOVA client agent."""
    
    @abstractmethod
    def metadata(self) -> dict:
        """Returns identity and version info."""
        pass
        
    @abstractmethod
    def supports_goal(self, goal: GoalContract) -> bool:
        """Returns True if this agent has expertise relevant to the goal."""
        pass
        
    @abstractmethod
    def reason(self, context: AgentContext) -> AgentReasoning:
        """Analyzes the goal and context, and returns a vote and rationale."""
        pass
