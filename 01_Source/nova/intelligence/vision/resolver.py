"""
Vision Resolver.
Resolves capabilities to active plugins.
"""
import logging
from typing import List
from nova.intelligence.vision.registry import VisionRegistry, IVisionPlugin
from nova.intelligence.vision.models import VisionRequest

logger = logging.getLogger(__name__)

class VisionResolver:
    """Maps a VisionRequest to a set of capable plugins."""
    
    def __init__(self, registry: VisionRegistry):
        self.registry = registry
        
    def resolve(self, request: VisionRequest) -> List[IVisionPlugin]:
        """Finds all plugins that satisfy the required capabilities."""
        plugins = []
        all_plugins = self.registry.get_all()
        
        if not request.required_capabilities:
            # If no specific capabilities requested, run everything available
            return all_plugins
            
        for plugin in all_plugins:
            # If the plugin offers ANY of the requested capabilities, we use it
            if any(cap in plugin.capabilities for cap in request.required_capabilities):
                plugins.append(plugin)
                
        logger.debug(f"Resolved {len(plugins)} plugins for requested capabilities {request.required_capabilities}")
        return plugins
