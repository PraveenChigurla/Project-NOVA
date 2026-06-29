"""
Project NOVA - Trust Framework Demonstration.
Simulates installing a safe package vs a malicious package under Enterprise policy.
"""

import sys
import logging
from nova.security.trust.models import PackageManifest, PolicyEnvironment
from nova.security.trust.framework import TrustFramework
from nova.security.trust.installer import PackageInstaller

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("nova.demo_trust")

def main():
    logger.info("Initializing Trust Framework under ENTERPRISE policy...")
    
    trust_framework = TrustFramework(policy_environment=PolicyEnvironment.ENTERPRISE)
    installer = PackageInstaller(trust_framework)
    
    # 1. Safe Package
    logger.info("\n--- SCENARIO 1: SAFE PACKAGE ---")
    safe_manifest = PackageManifest(
        name="github_login",
        version="1.0.0",
        publisher="OpenNOVA Foundation",
        permissions_requested=["browser.navigate", "keyboard.type"],
        has_signature=True,
        has_sbom=True
    )
    installer.install("/downloads/github_login.nova", safe_manifest)
    
    # 2. Malicious Package
    logger.info("\n--- SCENARIO 2: MALICIOUS PACKAGE ---")
    malicious_manifest = PackageManifest(
        name="free_bitcoin_miner",
        version="6.6.6",
        publisher="UnknownHacker99",
        permissions_requested=["vault.read", "fs.delete", "process.kill"],
        has_signature=False, # Unsigned
        has_sbom=False       # No BOM
    )
    installer.install("/downloads/free_bitcoin_miner.nova", malicious_manifest)
    
if __name__ == "__main__":
    if sys.platform != 'win32':
        logger.error("This demonstration requires Windows.")
        sys.exit(1)
    main()
