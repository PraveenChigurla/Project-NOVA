"""
Trust Framework.
The central coordinator for evaluating package trust.
"""
import logging
from nova.security.trust.models import PackageManifest, TrustEvaluation, PolicyEnvironment
from nova.security.trust.policy import PolicyEngine
from nova.security.trust.analyzers import SignatureValidator, SBOMValidator

logger = logging.getLogger(__name__)

class TrustFramework:
    """Evaluates a package before allowing installation."""
    
    def __init__(self, policy_environment: PolicyEnvironment = PolicyEnvironment.PERSONAL):
        self.policy_engine = PolicyEngine(policy_environment)
        self.signature_validator = SignatureValidator()
        self.sbom_validator = SBOMValidator()
        
    def evaluate_package(self, manifest: PackageManifest) -> TrustEvaluation:
        logger.info(f"TrustFramework beginning evaluation for '{manifest.name} v{manifest.version}'")
        
        reasons = []
        is_trusted = True
        
        # 1. Policy Evaluation
        policy_pass, policy_reasons = self.policy_engine.evaluate(manifest)
        if not policy_pass:
            is_trusted = False
            reasons.extend(policy_reasons)
            
        # 2. Signature Evaluation
        # We only strictly fail on signature if policy dictates it (handled in PolicyEngine)
        # But we can still log warnings or informational reasons.
        sig_pass, sig_reasons = self.signature_validator.validate(manifest)
        if not sig_pass:
            reasons.extend(sig_reasons)
            
        return TrustEvaluation(
            is_trusted=is_trusted,
            reasons=reasons,
            policy_applied=self.policy_engine.environment
        )
