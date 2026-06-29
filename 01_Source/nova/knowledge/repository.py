"""
Knowledge Repository.
The safe, isolated storage for portable Knowledge artifacts (separate from sovereign Memory).
"""
import logging
from typing import Dict, List
from nova.knowledge.models import KnowledgePackage

logger = logging.getLogger(__name__)

class KnowledgeRepository:
    
    def __init__(self):
        self._store: Dict[str, KnowledgePackage] = {}
        
    def store(self, pkg: KnowledgePackage):
        """Saves an installed knowledge package to the local registry."""
        self._store[pkg.manifest.name] = pkg
        logger.info(f"KnowledgeRepository: Stored '{pkg.manifest.name}'.")
        
    def get_all(self) -> List[KnowledgePackage]:
        return list(self._store.values())
        
    def get_by_target(self, target: str) -> List[KnowledgePackage]:
        """Retrieves knowledge relating to a specific skill or goal."""
        return [p for p in self._store.values() if p.data.target == target]
