"""
Permission Policy Engine.
Evaluates if a capability is inherently allowed to request a scope based on system rules.
"""

from typing import List, Dict
import logging

from nova.security.permissions.models import PermissionScope, PermissionRequest, PermissionDecision, PermissionResult

logger = logging.getLogger(__name__)

class PermissionPolicy:
    """
    Defines the baseline security rules for capabilities.
    """
    def __init__(self):
        # A simple RBAC/Capability-to-Scope mapping for Phase 1.
        # Format: { capability_id: [allowed_scopes] }
        # Example: "com.nova.hello": [PermissionScope.OS_FILES_READ]
        self._allowed_mappings: Dict[str, List[PermissionScope]] = {
            "com.nova.hello": [PermissionScope.OS_FILES_READ]
        }

    def can_request(self, capability_id: str, scope: PermissionScope) -> bool:
        """Check if a capability is even allowed to ask for this permission."""
        allowed_scopes = self._allowed_mappings.get(capability_id, [])
        return scope in allowed_scopes

class PermissionValidator:
    """
    Executes the policy evaluation.
    Extension point for future complex trust-level validations.
    """
    def __init__(self, policy: PermissionPolicy):
        self._policy = policy

    def evaluate_baseline(self, request: PermissionRequest) -> PermissionResult:
        """
        Evaluate if the capability fundamentally has the right to request this scope.
        If it does not, it returns a hard DENY.
        If it does, it returns a PROMPT, meaning it requires explicit granting from the Registry/User.
        """
        if not self._policy.can_request(request.capability_id, request.scope):
            return PermissionResult(
                decision=PermissionDecision.DENY,
                message=f"Policy Engine Hard Deny: {request.capability_id} is not authorized to request {request.scope.value}"
            )
            
        return PermissionResult(
            decision=PermissionDecision.PROMPT,
            message=f"Policy Engine Prompt: {request.capability_id} is allowed to request {request.scope.value}. Awaiting grant."
        )
