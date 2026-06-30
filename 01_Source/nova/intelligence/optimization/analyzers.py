"""
Analyzers.
Scans the Event Chronicle to detect statistical patterns and anomalies.
"""
import logging
from typing import List, Optional
from nova.intelligence.world.chronicle import EventChronicle, LifeEvent
from nova.intelligence.optimization.models import OptimizationProposal, OptimizationCategory

logger = logging.getLogger(__name__)

class ExecutionAnalyzer:
    """Analyzes execution patterns for inefficiencies."""
    
    def analyze_redundancy(self, chronicle: EventChronicle, goal_id: str) -> Optional[OptimizationProposal]:
        logger.debug(f"ExecutionAnalyzer checking redundancy for {goal_id}...")
        
        events = chronicle.get_events()
        
        # Count total executions
        total_executions = sum(1 for e in events if e.event_type == "GoalReceived" and e.details.get("goal_id", "") == goal_id)
        
        if total_executions < 10: # We need statistical significance
            return None
            
        # Count how many times a step was skipped due to already being open
        skipped_count = sum(1 for e in events if e.event_type == "ExecutionStepSkipped" and e.details.get("goal_id", "") == goal_id)
        
        skip_ratio = skipped_count / total_executions
        
        if skip_ratio > 0.8: # If we skip this step 80% of the time
            logger.info(f"Anomaly Detected: {goal_id} skips execution steps {skip_ratio*100:.1f}% of the time.")
            return OptimizationProposal(
                proposal_id=f"opt_redundancy_{goal_id}",
                category=OptimizationCategory.UNUSED_STEP,
                affected_skill=goal_id,
                reason=f"Execution steps for this goal are skipped {skip_ratio*100:.1f}% of the time due to pre-existing World Model state.",
                confidence=skip_ratio,
                expected_benefit="Reduce planner latency by executing a pre-flight state check before generating the full plan.",
                requires_approval=True
            )
            
        return None
