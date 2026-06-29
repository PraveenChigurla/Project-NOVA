"""
Knowledge Importer.
Safely ingests .kpkg artifacts by routing them through the Trust Framework.
"""
import logging
from nova.knowledge.models import KnowledgePackage
from nova.knowledge.repository import KnowledgeRepository
from nova.security.trust.framework import TrustFramework

logger = logging.getLogger(__name__)

class KnowledgeImporter:
    
    def __init__(self, trust_framework: TrustFramework, repository: KnowledgeRepository):
        self.trust = trust_framework
        self.repo = repository
        
    def import_package(self, pkg: KnowledgePackage) -> bool:
        """Attempts to install a knowledge package."""
        logger.info(f"KnowledgeImporter: Attempting to ingest '{pkg.manifest.name}'...")
        
        # 1. Trust Evaluation
        # Because KnowledgeManifest inherits from PackageManifest, we can pass it directly to the TrustFramework.
        evaluation = self.trust.evaluate_package(pkg.manifest)
        
        if not evaluation.is_trusted:
            logger.error(f"Knowledge Import Failed: Package '{pkg.manifest.name}' rejected by Trust Framework.")
            for r in evaluation.reasons:
                logger.error(f"  - {r}")
            return False
            
        # 2. Additional Knowledge-Specific Checks
        if pkg.manifest.evidence_score < 0.5:
            logger.warning(f"Knowledge Import Rejected: Evidence score ({pkg.manifest.evidence_score}) is below the acceptable threshold.")
            return False
            
        # 3. Store
        self.repo.store(pkg)
        logger.info(f"Knowledge Import Success: '{pkg.manifest.name}' has been added to the local repository.")
        return True
