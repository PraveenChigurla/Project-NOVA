"""
Skill Loader & Registry.
Discovers, parses, and maintains portable Skill Packages.
"""
import os
import yaml
import logging
from typing import Dict, List, Optional

from nova.skills.models import SkillManifest

logger = logging.getLogger(__name__)

class SkillRegistry:
    """Maintains the catalogue of active Skill Packages."""
    
    def __init__(self):
        self._skills: Dict[str, SkillManifest] = {}
        
    def register(self, manifest: SkillManifest) -> None:
        if manifest.id in self._skills:
            logger.warning(f"Skill '{manifest.id}' is already registered. Overwriting with v{manifest.version}.")
        self._skills[manifest.id] = manifest
        logger.debug(f"Registered Skill: {manifest.id} v{manifest.version}")
        
    def get(self, skill_id: str) -> Optional[SkillManifest]:
        return self._skills.get(skill_id)
        
    def get_all(self) -> List[SkillManifest]:
        return list(self._skills.values())

class SkillLoader:
    """Discovers and parses portable Skill Packages from disk."""
    
    def __init__(self, registry: SkillRegistry):
        self.registry = registry
        
    def discover_and_load(self, base_path: str) -> int:
        """Scans a directory for skill packages and loads them into the registry."""
        if not os.path.exists(base_path):
            logger.warning(f"Skill directory '{base_path}' does not exist.")
            return 0
            
        loaded_count = 0
        for item in os.listdir(base_path):
            skill_dir = os.path.join(base_path, item)
            if os.path.isdir(skill_dir):
                manifest = self._load_skill(skill_dir)
                if manifest:
                    self.registry.register(manifest)
                    loaded_count += 1
                    
        logger.info(f"Loaded {loaded_count} skills from {base_path}")
        return loaded_count
        
    def _load_skill(self, skill_dir: str) -> Optional[SkillManifest]:
        """Parses `skill.yaml` inside a specific package folder."""
        manifest_path = os.path.join(skill_dir, "skill.yaml")
        
        if not os.path.exists(manifest_path):
            logger.debug(f"Skipping {skill_dir}: No skill.yaml found.")
            return None
            
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                
            manifest = SkillManifest(**data)
            manifest.package_path = skill_dir
            return manifest
            
        except Exception as e:
            logger.error(f"Failed to load skill from {manifest_path}: {e}")
            return None
