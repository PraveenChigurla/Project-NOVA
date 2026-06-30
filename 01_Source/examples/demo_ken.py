"""
Project NOVA - Knowledge Exchange Network Demonstration.
Simulates a Desktop node exporting an optimization and a Laptop node importing it via the Trust Framework.
"""
import sys
import logging
from nova.intelligence.optimization.models import OptimizationProposal, OptimizationCategory
from nova.security.trust.framework import TrustFramework, PolicyEnvironment
from nova.knowledge.manager import KnowledgeManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("nova.demo_ken")

def main():
    logger.info("Initializing Knowledge Exchange Network (KEN)...\n")
    
    # Simulate two independent environments
    desktop_trust = TrustFramework(PolicyEnvironment.PERSONAL)
    desktop_ken = KnowledgeManager(desktop_trust)
    
    laptop_trust = TrustFramework(PolicyEnvironment.ENTERPRISE)
    laptop_ken = KnowledgeManager(laptop_trust)
    
    # 1. Desktop generates an optimization based on its local Event Chronicle
    logger.info("--- SCENARIO: DESKTOP LEARNS AND EXPORTS ---")
    local_optimization = OptimizationProposal(
        proposal_id="opt_001",
        category=OptimizationCategory.EXECUTION_ORDER,
        affected_skill="prepare_workspace",
        reason="Chrome startup delayed execution. Moving to end of plan saves 2 seconds.",
        confidence=0.94,
        expected_benefit="2s reduction in startup time",
        requires_approval=True
    )
    
    # 2. Desktop exports it to a portable .kpkg
    knowledge_pkg = desktop_ken.export_optimization_to_knowledge(local_optimization, "Desktop_Owner")
    logger.info(f"Generated portable artifact: '{knowledge_pkg.manifest.name}.kpkg'")
    
    # 3. Simulate transmitting the file to the Laptop (USB, LAN, Cloud, etc)
    logger.info("\n--- SCENARIO: LAPTOP IMPORTS KNOWLEDGE ---")
    logger.info(f"Laptop received '{knowledge_pkg.manifest.name}.kpkg' via arbitrary transport.")
    
    # 4. Laptop attempts to install it
    success = laptop_ken.import_knowledge(knowledge_pkg)
    
    if success:
        logger.info("\nSUCCESS: Laptop has successfully imported the optimization.")
        logger.info("Note: Laptop did NOT import Desktop's memory, event chronicle, or vault secrets.")
        logger.info("Only abstracted, cryptographically signed *Knowledge* was exchanged.")
    else:
        logger.error("\nFAILURE: Laptop rejected the knowledge package.")
        
if __name__ == "__main__":
    if sys.platform != 'win32':
        logger.error("This demonstration requires Windows.")
        sys.exit(1)
    main()
