"""
Knowledge Manager.
Orchestrates the export, import, and storage of portable Knowledge artifacts.
"""
import logging
from nova.intelligence.optimization.models import OptimizationProposal
from nova.knowledge.exporter import KnowledgeExporter
from nova.knowledge.importer import KnowledgeImporter
from nova.knowledge.repository import KnowledgeRepository
from nova.security.trust.framework import TrustFramework

logger = logging.getLogger(__name__)

class KnowledgeManager:
    """The entrypoint for the Knowledge Exchange Network (KEN)."""
    
    def __init__(self, trust_framework: TrustFramework):
        self.repository = KnowledgeRepository()
        self.exporter = KnowledgeExporter()
        self.importer = KnowledgeImporter(trust_framework, self.repository)
        
    def export_optimization_to_knowledge(self, proposal: OptimizationProposal, publisher: str):
        """Converts an internal optimization into a portable .kpkg object."""
        return self.exporter.export_optimization(proposal, publisher)
        
    def import_knowledge(self, package) -> bool:
        """Attempts to install a .kpkg object into the local runtime."""
        return self.importer.import_package(package)
