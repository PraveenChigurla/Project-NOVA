"""
Permission Manager.
The primary entry point for capability authorization.
"""

from typing import Optional
from datetime import datetime
import logging

from nova.security.permissions.models import PermissionRequest, PermissionResult, PermissionDecision, PermissionScope, _now
from nova.security.permissions.registry import PermissionRegistry
from nova.security.permissions.policy import PermissionPolicy, PermissionValidator

logger = logging.getLogger(__name__)

class PermissionManager:
    """
    The central authorization gateway.
    Capabilities invoke this to request execution rights.
    """
    def __init__(self):
        self.registry = PermissionRegistry()
        self.policy = PermissionPolicy()
        self.validator = PermissionValidator(self.policy)

    async def grant(self, capability_id: str, scope: PermissionScope, expires_at: Optional[datetime] = None) -> None:
        """Grant a permission to a capability."""
        await self.registry.grant(capability_id, scope, expires_at)

    async def revoke(self, capability_id: str, scope: PermissionScope) -> None:
        """Revoke a permission."""
        await self.registry.revoke(capability_id, scope)

    async def evaluate(self, request: PermissionRequest) -> PermissionResult:
        """
        Evaluate a capability's request to access a scope.
        1. Check baseline policy.
        2. Check registry for active grants.
        3. Enforce expiration times.
        4. Generate audit log.
        """
        # Step 1: Base Policy check
        baseline_result = self.validator.evaluate_baseline(request)
        if baseline_result.decision == PermissionDecision.DENY:
            logger.warning(f"AUDIT [DENY]: {request.capability_id} -> {request.scope.value} (Policy Reject)")
            return baseline_result

        # Step 2: Registry check
        has_grant, expires_at = await self.registry.get_grant(request.capability_id, request.scope)
        
        if not has_grant:
            msg = f"AUDIT [PROMPT]: {request.capability_id} -> {request.scope.value} (No active grant found)"
            logger.info(msg)
            return PermissionResult(decision=PermissionDecision.PROMPT, message=msg)
            
        # Step 3: Expiration check
        if expires_at and expires_at < _now():
            await self.registry.revoke(request.capability_id, request.scope)
            msg = f"AUDIT [DENY]: {request.capability_id} -> {request.scope.value} (Grant expired at {expires_at})"
            logger.warning(msg)
            return PermissionResult(decision=PermissionDecision.DENY, message=msg)

        # Step 4: Allow
        msg = f"AUDIT [ALLOW]: {request.capability_id} -> {request.scope.value} (Authorized)"
        logger.info(msg)
        return PermissionResult(
            decision=PermissionDecision.ALLOW,
            message=msg,
            expires_at=expires_at
        )
