"""
Permission Registry.
Stores and tracks active capability grants (both persistent and temporary).
"""

from typing import Dict, Optional
import asyncio
import logging
from datetime import datetime

from nova.security.permissions.models import PermissionScope

logger = logging.getLogger(__name__)

class PermissionRegistry:
    """
    Thread-safe storage for capability permission grants.
    """
    def __init__(self):
        # Format: { capability_id: { PermissionScope: expires_at (or None for persistent) } }
        self._grants: Dict[str, Dict[PermissionScope, Optional[datetime]]] = {}
        self._lock = asyncio.Lock()

    async def grant(self, capability_id: str, scope: PermissionScope, expires_at: Optional[datetime] = None) -> None:
        """Grant a permission to a capability."""
        async with self._lock:
            if capability_id not in self._grants:
                self._grants[capability_id] = {}
            
            self._grants[capability_id][scope] = expires_at
            
            if expires_at:
                logger.info(f"Granted temporary '{scope.value}' to '{capability_id}' until {expires_at}")
            else:
                logger.info(f"Granted persistent '{scope.value}' to '{capability_id}'")

    async def revoke(self, capability_id: str, scope: PermissionScope) -> None:
        """Revoke a permission from a capability."""
        async with self._lock:
            if capability_id in self._grants and scope in self._grants[capability_id]:
                del self._grants[capability_id][scope]
                logger.warning(f"Revoked '{scope.value}' from '{capability_id}'")

    async def get_grant(self, capability_id: str, scope: PermissionScope) -> Optional[Optional[datetime]]:
        """
        Check if a grant exists.
        Returns None if no grant exists.
        Returns datetime if temporary grant exists.
        Returns `False` implicitly if you check the tuple? No, let's return a tuple (exists, expires_at).
        Actually, raising KeyError if not found is better, or returning a specific structure.
        Let's return a dict with 'granted': bool and 'expires_at': datetime.
        """
        async with self._lock:
            if capability_id in self._grants and scope in self._grants[capability_id]:
                # Found the grant, return the expiration time (which might be None for persistent)
                return True, self._grants[capability_id][scope]
            return False, None
