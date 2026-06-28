"""
Provider Registry.
Thread-safe, asynchronous registry for managing provider lifecycles.
"""

from typing import Dict, List, Optional
import asyncio
import logging

from nova.providers.base import Provider, ProviderState, ProviderHealth, ProviderType

logger = logging.getLogger(__name__)

class ProviderRegistryError(Exception):
    """Base exception for provider registry operations."""
    pass

class ProviderRegistry:
    """
    Authoritative, thread-safe runtime registry for all providers.
    """
    def __init__(self):
        self._providers: Dict[str, Provider] = {}
        self._lock = asyncio.Lock()
        
    async def register(self, provider: Provider) -> None:
        """Register a new provider."""
        async with self._lock:
            pid = provider.metadata.id
            if pid in self._providers:
                raise ProviderRegistryError(f"Provider with ID '{pid}' is already registered.")
            
            for existing in self._providers.values():
                if existing.metadata.name == provider.metadata.name:
                    raise ProviderRegistryError(f"Provider with name '{provider.metadata.name}' is already registered.")
            
            self._providers[pid] = provider
            await provider.system_register()
            logger.info(f"Registered Provider: {pid}")

    async def unregister(self, provider_id: str) -> None:
        """Unregister a provider."""
        async with self._lock:
            if provider_id not in self._providers:
                raise ProviderRegistryError(f"Provider '{provider_id}' not found.")
            
            prov = self._providers[provider_id]
            if prov.state != ProviderState.SHUTDOWN:
                raise ProviderRegistryError(f"Provider '{provider_id}' must be in SHUTDOWN state before unregistering.")
                
            del self._providers[provider_id]
            logger.info(f"Unregistered Provider: {provider_id}")

    # -------------------------------------------------------------------------
    # Query APIs (Thread-safe reads)
    # -------------------------------------------------------------------------

    async def get(self, provider_id: str) -> Optional[Provider]:
        async with self._lock:
            return self._providers.get(provider_id)

    async def get_by_type(self, provider_type: ProviderType) -> List[Provider]:
        async with self._lock:
            return [p for p in self._providers.values() if p.metadata.type == provider_type]

    async def enumerate_providers(self) -> List[Provider]:
        async with self._lock:
            return list(self._providers.values())

    async def query_health(self) -> Dict[str, ProviderHealth]:
        health_report = {}
        async with self._lock:
            provs = list(self._providers.values())
            
        for prov in provs:
            health = await prov.on_health_check()
            health_report[prov.metadata.id] = health
            
        return health_report
