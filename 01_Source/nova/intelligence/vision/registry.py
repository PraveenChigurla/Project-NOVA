"""
Vision Registry.
Maintains a catalog of active visual capabilities/providers.
"""

from typing import Dict, List, Optional
import logging
from abc import ABC, abstractmethod

from nova.intelligence.vision.models import VisionRequest, VisionResult

logger = logging.getLogger(__name__)

class IVisionPlugin(ABC):
    """Abstract interface for a Vision Plugin (e.g. OCR, Object Detection)."""
    @property
    @abstractmethod
    def plugin_id(self) -> str:
        pass
        
    @property
    @abstractmethod
    def capabilities(self) -> List[str]:
        """e.g. ['ocr'], ['object_detection']"""
        pass
        
    @abstractmethod
    async def process(self, request: VisionRequest) -> VisionResult:
        """Processes the image and returns a partial VisionResult to be aggregated."""
        pass

class VisionRegistry:
    """Manages the catalog of known vision plugins."""
    
    def __init__(self):
        self._plugins: Dict[str, IVisionPlugin] = {}
        
    def register(self, plugin: IVisionPlugin) -> None:
        """Registers a new vision plugin."""
        if plugin.plugin_id in self._plugins:
            logger.warning(f"Vision Plugin '{plugin.plugin_id}' is already registered. Overwriting.")
        self._plugins[plugin.plugin_id] = plugin
        logger.debug(f"Registered vision plugin: {plugin.plugin_id} with capabilities: {plugin.capabilities}")
        
    def get(self, plugin_id: str) -> Optional[IVisionPlugin]:
        """Retrieves a plugin by ID."""
        return self._plugins.get(plugin_id)
        
    def get_all(self) -> List[IVisionPlugin]:
        """Returns all registered plugins."""
        return list(self._plugins.values())
