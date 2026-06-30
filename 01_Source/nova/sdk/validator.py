"""
NOVA SDK Validator.
Ensures extensions conform to the required contracts before they are packaged.
"""
import os
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ValidatorError(Exception):
    pass

class ExtensionValidator:
    """Validates the structure and contracts of an extension."""
    
    def validate(self, project_dir: str) -> bool:
        """Runs the validation suite against a project directory."""
        logger.info(f"Validating extension at '{project_dir}'...")
        
        try:
            self._validate_manifest(project_dir)
            self._validate_structure(project_dir)
            # In a real SDK, we would do AST parsing or dynamic importing here to check class signatures
            logger.info("Validation Passed.")
            return True
        except ValidatorError as e:
            logger.error(f"Validation Failed: {e}")
            return False
            
    def _validate_manifest(self, project_dir: str):
        manifest_path = os.path.join(project_dir, "manifest.json")
        if not os.path.exists(manifest_path):
            raise ValidatorError("Missing manifest.json")
            
        with open(manifest_path, "r") as f:
            manifest = json.load(f)
            
        required_keys = ["name", "version", "type", "permissions", "dependencies"]
        for key in required_keys:
            if key not in manifest:
                raise ValidatorError(f"Manifest missing required key: {key}")
                
    def _validate_structure(self, project_dir: str):
        src_path = os.path.join(project_dir, "src")
        if not os.path.exists(src_path):
            raise ValidatorError("Missing 'src/' directory.")
            
        main_py = os.path.join(src_path, "main.py")
        if not os.path.exists(main_py):
            raise ValidatorError("Missing 'src/main.py' entrypoint.")
