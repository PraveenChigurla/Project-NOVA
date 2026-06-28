"""
Provider Discovery and Loading.
Provides mechanisms to find and instantiate providers.
"""

from typing import List
import logging

from nova.providers.base import Provider, ProviderMetadata, ProviderType
from nova.providers.mock_provider import MockProvider

logger = logging.getLogger(__name__)

class ProviderDiscovery:
    """
    Discovers providers from the environment or built-in modules.
    For Phase 1, it manually loads the MockProvider reference implementation.
    """
    
    def discover_builtins(self) -> List[Provider]:
        """Discover built-in providers statically defined in the codebase."""
        providers = []
        
        meta = ProviderMetadata(
            id="com.nova.provider.mock",
            name="Mock Provider",
            version="1.0.0",
            type=ProviderType.MOCK,
            description="A minimal reference provider"
        )
        
        mock_prov = MockProvider(meta)
        providers.append(mock_prov)
        
        import os
        if os.name == 'nt':
            from nova.providers.desktop.provider import WindowsDesktopProvider
            desktop_meta = ProviderMetadata(
                id="com.nova.provider.desktop",
                name="Windows Desktop Provider",
                version="1.0.0",
                type=ProviderType.DESKTOP,
                description="Provides native integration with Windows OS"
            )
            desktop_prov = WindowsDesktopProvider(desktop_meta)
            providers.append(desktop_prov)
        
        logger.info(f"Discovered {len(providers)} built-in providers.")
        return providers

class ProviderLoader:
    """
    Loads discovered providers into a registry.
    """
    def __init__(self, registry, discovery: ProviderDiscovery):
        self._registry = registry
        self._discovery = discovery
        
    async def load_all(self) -> None:
        """Discover and register all available providers."""
        builtins = self._discovery.discover_builtins()
        
        for prov in builtins:
            try:
                await self._registry.register(prov)
            except Exception as e:
                logger.error(f"Failed to load provider {prov.metadata.id}: {e}")
