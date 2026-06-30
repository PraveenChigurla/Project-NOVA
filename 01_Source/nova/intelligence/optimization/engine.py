"""
Optimization Engine.
Generates human-readable Optimization Proposals by orchestrating Analyzers over the Event Chronicle.
"""
import logging
from typing import List
from nova.intelligence.world.chronicle import EventChronicle
from nova.intelligence.optimization.models import OptimizationProposal
from nova.intelligence.optimization.analyzers import ExecutionAnalyzer

logger = logging.getLogger(__name__)

class OptimizationEngine:
    """The continuous improvement subsystem of NOVA."""
    
    def __init__(self, chronicle: EventChronicle):
        self.chronicle = chronicle
        self.execution_analyzer = ExecutionAnalyzer()
        
    def generate_proposals(self) -> List[OptimizationProposal]:
        """Scans the history and returns proposals for human review."""
        logger.info("OptimizationEngine starting chronicle analysis...")
        
        proposals = []
        
        # In a real system, we would dynamically extract unique goal IDs from the chronicle
        # For this sprint, we analyze 'prepare_workspace'
        proposal = self.execution_analyzer.analyze_redundancy(self.chronicle, "prepare_workspace")
        if proposal:
            proposals.append(proposal)
            
        logger.info(f"OptimizationEngine generated {len(proposals)} proposals.")
        return proposals
