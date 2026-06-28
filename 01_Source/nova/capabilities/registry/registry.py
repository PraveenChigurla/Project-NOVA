"""
Capability Registry.
Thread-safe, asynchronous registry for managing capability lifecycles and metadata querying.
"""

from typing import Dict, List, Optional, Any
import asyncio
import logging

from nova.capabilities.base import Capability, CapabilityState, CapabilityHealth
from nova.capabilities.registry.validator import DependencyValidator

logger = logging.getLogger(__name__)

class CapabilityRegistryError(Exception):
    """Base exception for registry operations."""
    pass

class CapabilityRegistry:
    """
    Authoritative, thread-safe runtime registry for all capabilities.
    """
    def __init__(self):
        self._capabilities: Dict[str, Capability] = {}
        self._lock = asyncio.Lock()
        
    async def register(self, capability: Capability) -> None:
        """Register a new capability, ensuring thread safety and uniqueness."""
        async with self._lock:
            cid = capability.metadata.id
            if cid in self._capabilities:
                raise CapabilityRegistryError(f"Capability with ID '{cid}' is already registered.")
            
            # Check for duplicate names
            for existing in self._capabilities.values():
                if existing.metadata.name == capability.metadata.name:
                    raise CapabilityRegistryError(f"Capability with name '{capability.metadata.name}' is already registered.")
            
            self._capabilities[cid] = capability
            await capability.system_register()
            logger.info(f"Registered Capability: {cid}")

    async def unregister(self, capability_id: str) -> None:
        """Unregister a capability. It must be cleanly shut down first."""
        async with self._lock:
            if capability_id not in self._capabilities:
                raise CapabilityRegistryError(f"Capability '{capability_id}' not found.")
            
            cap = self._capabilities[capability_id]
            if cap.state != CapabilityState.SHUTDOWN:
                raise CapabilityRegistryError(f"Capability '{capability_id}' must be in SHUTDOWN state before unregistering.")
                
            del self._capabilities[capability_id]
            logger.info(f"Unregistered Capability: {capability_id}")

    # -------------------------------------------------------------------------
    # Query APIs (Thread-safe reads)
    # -------------------------------------------------------------------------

    async def get(self, capability_id: str) -> Optional[Capability]:
        """Lookup by capability ID."""
        async with self._lock:
            return self._capabilities.get(capability_id)

    async def get_by_name(self, name: str) -> Optional[Capability]:
        """Lookup by capability name."""
        async with self._lock:
            for cap in self._capabilities.values():
                if cap.metadata.name == name:
                    return cap
        return None

    async def get_by_tag(self, tag: str) -> List[Capability]:
        """Find all capabilities containing a specific tag."""
        async with self._lock:
            return [cap for cap in self._capabilities.values() if tag in cap.metadata.tags]

    async def get_by_intent(self, intent: str) -> List[Capability]:
        """Find all capabilities supporting a specific intent."""
        async with self._lock:
            return [cap for cap in self._capabilities.values() if intent in cap.metadata.supported_intents]

    async def get_by_permission(self, permission: str) -> List[Capability]:
        """Find all capabilities that declare a specific OS permission."""
        async with self._lock:
            return [cap for cap in self._capabilities.values() if permission in cap.metadata.permissions_required]

    async def enumerate_capabilities(self) -> List[Capability]:
        """Return all registered capabilities."""
        async with self._lock:
            return list(self._capabilities.values())

    async def query_health(self) -> Dict[str, CapabilityHealth]:
        """Poll the health status of all registered capabilities."""
        health_report = {}
        # Make a copy of values inside the lock to avoid holding the lock during async operations
        async with self._lock:
            caps = list(self._capabilities.values())
            
        for cap in caps:
            health = await cap.on_health_check()
            health_report[cap.metadata.id] = health
            
        return health_report

    # -------------------------------------------------------------------------
    # Validation API
    # -------------------------------------------------------------------------
    
    async def validate_dependencies(self) -> None:
        """
        Validate the dependency graph of all currently registered capabilities.
        Raises an exception if the graph contains missing or circular dependencies.
        """
        async with self._lock:
            validator = DependencyValidator()
            for cap in self._capabilities.values():
                validator.add_capability(cap.metadata.id, cap.metadata.dependencies)
                
            # Will raise DependencyError if validation fails
            validator.validate_graph()
