"""
Knowledge Exporter.
Converts local learning (like Optimization Proposals) into portable .kpkg artifacts.
"""
import logging
import json
from nova.intelligence.optimization.models import OptimizationProposal
from nova.knowledge.models import KnowledgeManifest, KnowledgeData, KnowledgePackage

logger = logging.getLogger(__name__)

class KnowledgeExporter:
    
    def export_optimization(self, proposal: OptimizationProposal, publisher: str) -> KnowledgePackage:
        logger.info(f"Exporting OptimizationProposal '{proposal.proposal_id}' to KnowledgePackage...")
        
        manifest = KnowledgeManifest(
            name=f"opt_{proposal.affected_skill}",
            version="1.0.0",
            publisher=publisher,
            permissions_requested=[], # Knowledge rarely needs active execution permissions
            has_signature=True,
            has_sbom=True,
            evidence_score=proposal.confidence,
            type="knowledge"
        )
        
        data = KnowledgeData(
            category=proposal.category.value,
            target=proposal.affected_skill,
            payload={
                "benefit": proposal.expected_benefit,
                "risk": proposal.risk
            }
        )
        
        pkg = KnowledgePackage(
            manifest=manifest,
            data=data,
            evidence_summary=proposal.reason
        )
        
        logger.info(f"KnowledgePackage '{manifest.name}' generated successfully.")
        return pkg
