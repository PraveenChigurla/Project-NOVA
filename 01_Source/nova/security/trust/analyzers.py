"""
Trust Analyzers.
Validates signatures, compatibility, and SBOMs.
"""
import logging
from typing import Tuple, List
from nova.security.trust.models import PackageManifest

logger = logging.getLogger(__name__)

class SignatureValidator:
    """Mocks PKI signature validation."""
    def validate(self, manifest: PackageManifest) -> Tuple[bool, List[str]]:
        if not manifest.has_signature:
            return False, ["Package is unsigned. Identity cannot be verified."]
        # In reality, verify the crypto signature here.
        return True, []

class SBOMValidator:
    """Mocks SBOM validation."""
    def validate(self, manifest: PackageManifest) -> Tuple[bool, List[str]]:
        if not manifest.has_sbom:
            return False, ["Package is missing an SBOM."]
        # In reality, parse the SBOM and check for known CVEs.
        return True, []
