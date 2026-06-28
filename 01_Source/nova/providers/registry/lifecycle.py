"""
Provider Lifecycle Coordinator.
Manages the booting and teardown of providers.
"""

from typing import Dict
import logging

from nova.providers.registry.registry import ProviderRegistry
from nova.providers.base import ProviderState

logger = logging.getLogger(__name__)

class ProviderLifecycleCoordinator:
    """
    Coordinates provider lifecycles. 
    Providers typically don't have deep inter-dependencies like Capabilities, 
    but they must be booted before Capabilities.
    """
    def __init__(self, registry: ProviderRegistry):
        self._registry = registry

    async def boot_all(self, global_config: Dict[str, dict]) -> None:
        """Initializes and starts all registered providers."""
        provs = await self._registry.enumerate_providers()
        
        for prov in provs:
            pid = prov.metadata.id
            config = global_config.get(pid, {})
            
            logger.info(f"Initializing Provider {pid}...")
            await prov.system_initialize(config)
            
            logger.info(f"Starting Provider {pid}...")
            await prov.system_start()
            
            if prov.state != ProviderState.READY:
                raise RuntimeError(f"Provider {pid} failed to reach READY state. Current: {prov.state}")
            logger.info(f"Provider {pid} successfully booted.")

    async def shutdown_all(self) -> None:
        """Shuts down all providers."""
        provs = await self._registry.enumerate_providers()
        
        for prov in provs:
            pid = prov.metadata.id
            if prov.state not in (ProviderState.SHUTDOWN, ProviderState.CREATED):
                logger.info(f"Shutting down Provider {pid}...")
                try:
                    await prov.system_shutdown()
                except Exception as e:
                    logger.error(f"Error shutting down Provider {pid}: {e}")
