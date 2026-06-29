"""
Package Installer.
Installs a package only if it passes the Trust Framework.
"""
import logging
from nova.security.trust.models import PackageManifest
from nova.security.trust.framework import TrustFramework

logger = logging.getLogger(__name__)

class PackageInstaller:
    """The gatekeeper for deploying code into the runtime."""
    
    def __init__(self, trust_framework: TrustFramework):
        self.trust = trust_framework
        
    def install(self, package_path: str, simulated_manifest: PackageManifest) -> bool:
        """
        Attempts to install a .nova package.
        In reality, this would unzip the package to a temp dir and parse manifest.json.
        """
        logger.info(f"Attempting to install package from '{package_path}'...")
        
        evaluation = self.trust.evaluate_package(simulated_manifest)
        
        if evaluation.is_trusted:
            logger.info(f"INSTALLATION SUCCESS: Package '{simulated_manifest.name}' passed trust evaluation.")
            # Move from temp dir to runtime extensions dir here.
            return True
        else:
            logger.error(f"INSTALLATION FAILED: Trust evaluation rejected '{simulated_manifest.name}'.")
            for reason in evaluation.reasons:
                logger.error(f"  - {reason}")
            # Delete the temp dir here.
            return False
