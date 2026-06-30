"""
Reflection Engine.
Compares the final World Model state against expectations to evaluate success.
"""
import logging
from typing import List, Dict, Any
from pydantic import BaseModel
from nova.intelligence.world.models import WorldGraph
from nova.intelligence.world.chronicle import EventChronicle

logger = logging.getLogger(__name__)

class ReflectionReport(BaseModel):
    success: bool
    deviations: List[str]
    memory_suggestions: List[str]

class ReflectionEngine:
    """Evaluates execution outcomes."""
    
    def __init__(self, world_graph: WorldGraph, chronicle: EventChronicle):
        self.world = world_graph
        self.chronicle = chronicle
        
    def evaluate(self, goal_id: str, expected_state: Dict[str, Any]) -> ReflectionReport:
        logger.info(f"Reflection Engine evaluating goal: '{goal_id}'")
        
        deviations = []
        
        # Example validation: if expected_state requires 'vscode' to be running
        if expected_state.get("require_vscode", False):
            vscode_entities = [e for e in self.world.entities.values() if e.type == "Application" and e.attributes.get("name") == "VS Code"]
            if not vscode_entities:
                deviations.append("Expected VS Code to be running, but it was not found in the World Graph.")
                
        # Did the planner skip something because it was already open?
        # We could mine the chronicle for this.
        skipped = any(e.event_type == "ExecutionStepSkipped" for e in self.chronicle.get_events())
        suggestions = []
        if skipped:
            suggestions.append("User often has tools already open. Consider making 'Check Workspace' a default sub-routine.")
            
        success = len(deviations) == 0
        
        self.chronicle.record("ReflectionCompleted", {"goal_id": goal_id, "success": success})
        
        report = ReflectionReport(success=success, deviations=deviations, memory_suggestions=suggestions)
        if success:
            logger.info("Evaluation: SUCCESS. Goal was achieved as expected.")
        else:
            logger.warning(f"Evaluation: DEVIATIONS DETECTED. {deviations}")
            
        return report
