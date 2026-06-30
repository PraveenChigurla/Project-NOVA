"""
Project NOVA - SDK Demonstration.
Programmatically simulates a developer using the CLI to build a 'Hello World' skill.
"""
import sys
import os
import shutil
import logging
from nova.sdk.generator import ProjectGenerator
from nova.sdk.validator import ExtensionValidator
from nova.sdk.simulator import ExtensionSimulator
from nova.sdk.packager import ExtensionPackager

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("nova.demo_sdk")

def main():
    logger.info("--- 1. PROJECT GENERATOR ---")
    logger.info("> nova new skill hello_world")
    generator = ProjectGenerator()
    
    # Clean up previous runs
    if os.path.exists("hello_world"):
        shutil.rmtree("hello_world")
    if os.path.exists("hello_world.nova"):
        os.remove("hello_world.nova")
        
    project_dir = generator.generate("skill", "hello_world")
    
    logger.info("\n--- 2. VALIDATOR ---")
    logger.info(f"> nova validate {project_dir}")
    validator = ExtensionValidator()
    if not validator.validate(project_dir):
        logger.error("Validation failed! Halting.")
        sys.exit(1)
        
    logger.info("\n--- 3. SIMULATOR ---")
    logger.info(f"> nova simulate {project_dir}")
    simulator = ExtensionSimulator()
    simulator.simulate(project_dir)
    
    logger.info("\n--- 4. PACKAGER ---")
    logger.info(f"> nova package {project_dir}")
    packager = ExtensionPackager()
    nova_file = packager.package(project_dir)
    
    logger.info("\n--- VERIFICATION ---")
    logger.info(f"Final Artifact: {os.path.abspath(nova_file)}")
    logger.info("This .nova file contains the verified manifest and source code, ready for distribution.")

if __name__ == "__main__":
    if sys.platform != 'win32':
        logger.error("This demonstration requires Windows.")
        sys.exit(1)
    main()
