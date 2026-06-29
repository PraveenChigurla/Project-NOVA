"""
Policy Engine.
Decides if a package should be installed based on environment constraints.
"""
import logging
from typing import List, Tuple
from nova.security.trust.models import PackageManifest, PolicyEnvironment

logger = logging.getLogger(__name__)

class PolicyEngine:
    """Evaluates package manifests against defined policies."""
    
    def __init__(self, environment: PolicyEnvironment = PolicyEnvironment.PERSONAL):
        self.environment = environment
        
    def evaluate(self, manifest: PackageManifest) -> Tuple[bool, List[str]]:
        """Returns (is_allowed, list_of_reasons)."""
        logger.info(f"PolicyEngine evaluating '{manifest.name}' under {self.environment.value} policy.")
        
        reasons = []
        is_allowed = True
        
        if self.environment == PolicyEnvironment.ENTERPRISE:
            if "vault.read" in manifest.permissions_requested or "vault.write" in manifest.permissions_requested:
                is_allowed = False
                reasons.append("ENTERPRISE POLICY: Direct Vault access is prohibited for third-party extensions.")
                
            if "fs.delete" in manifest.permissions_requested:
                is_allowed = False
                reasons.append("ENTERPRISE POLICY: File deletion capabilities are prohibited.")
                
            if not manifest.has_sbom:
                is_allowed = False
                reasons.append("ENTERPRISE POLICY: Missing Software Bill of Materials (SBOM).")
                
        if self.environment == PolicyEnvironment.STRICT:
            if not manifest.has_signature:
                is_allowed = False
                reasons.append("STRICT POLICY: Unsigned packages are strictly prohibited.")
                
        if is_allowed:
            logger.info("PolicyEngine: Package complies with environment policies.")
        else:
            logger.warning(f"PolicyEngine: Package rejected. {reasons}")
            
        return is_allowed, reasons
