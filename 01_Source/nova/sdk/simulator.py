"""
NOVA SDK Simulator.
Provides a mock runtime for testing extensions without interacting with the real OS.
"""
import logging

logger = logging.getLogger(__name__)

class ExtensionSimulator:
    """Simulates the NOVA runtime."""
    
    def simulate(self, project_dir: str):
        """Runs the extension inside a mocked runtime container."""
        logger.info(f"--- STARTING SIMULATOR for {project_dir} ---")
        
        # In a real implementation:
        # 1. We would dynamically load the module from src/main.py
        # 2. We would inject MockProviders (e.g. MockWebProvider, MockScreenCapture)
        # 3. We would execute the workflow defined by the skill.
        
        logger.info("Initializing Mock World Graph...")
        logger.info("Initializing Mock Providers...")
        logger.info("Loading Extension Code...")
        
        logger.info("\n[SIMULATED EXECUTION]")
        logger.info("Step 1: Mock Workflow Step 1 executed successfully.")
        logger.info("Step 2: Mock Workflow Step 2 executed successfully.")
        
        logger.info("\n--- SIMULATION COMPLETE ---")
        logger.info("Result: SUCCESS")
