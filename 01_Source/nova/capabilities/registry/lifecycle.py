"""
Capability Lifecycle Coordinator.
Manages the topological booting and teardown of the registry capabilities.
"""

from typing import List, Dict, Set
import asyncio
import logging

from nova.capabilities.registry.registry import CapabilityRegistry
from nova.capabilities.base import CapabilityState

logger = logging.getLogger(__name__)

class LifecycleCoordinator:
    """
    Coordinates capability lifecycles according to dependency boundaries.
    """
    def __init__(self, registry: CapabilityRegistry):
        self._registry = registry

    def _get_topological_order(self, capabilities: List) -> List:
        """
        Returns capabilities sorted topologically (dependencies first).
        Assumes the graph has already been validated against cycles.
        """
        visited: Set[str] = set()
        ordered_caps = []
        cap_map = {c.metadata.id: c for c in capabilities}

        def dfs(cap_id: str):
            if cap_id in visited:
                return
            visited.add(cap_id)
            cap = cap_map.get(cap_id)
            if not cap:
                return
            for dep_id in cap.metadata.dependencies:
                dfs(dep_id)
            ordered_caps.append(cap)

        for cap in capabilities:
            dfs(cap.metadata.id)
            
        return ordered_caps

    async def boot_all(self, global_config: Dict[str, dict]) -> None:
        """
        Initializes and starts all registered capabilities in dependency order.
        """
        # Validate before booting
        await self._registry.validate_dependencies()
        
        caps = await self._registry.enumerate_capabilities()
        sorted_caps = self._get_topological_order(caps)
        
        for cap in sorted_caps:
            cid = cap.metadata.id
            config = global_config.get(cid, {})
            
            logger.info(f"Initializing {cid}...")
            await cap.system_initialize(config)
            
            logger.info(f"Starting {cid}...")
            await cap.system_start()
            
            if cap.state != CapabilityState.READY:
                raise RuntimeError(f"Capability {cid} failed to reach READY state. Current: {cap.state}")
            logger.info(f"Capability {cid} successfully booted.")

    async def shutdown_all(self) -> None:
        """
        Shuts down all capabilities in reverse dependency order.
        """
        caps = await self._registry.enumerate_capabilities()
        sorted_caps = self._get_topological_order(caps)
        reversed_caps = reversed(sorted_caps)
        
        for cap in reversed_caps:
            cid = cap.metadata.id
            if cap.state not in (CapabilityState.SHUTDOWN, CapabilityState.CREATED):
                logger.info(f"Shutting down {cid}...")
                try:
                    await cap.system_shutdown()
                except Exception as e:
                    logger.error(f"Error shutting down {cid}: {e}")
