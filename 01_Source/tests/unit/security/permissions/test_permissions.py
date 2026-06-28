"""
Tests for the Permission Framework.
"""

import pytest
from datetime import datetime, timezone, timedelta
import asyncio

from nova.security.permissions import (
    PermissionManager, 
    PermissionRequest, 
    PermissionScope, 
    PermissionDecision
)

@pytest.fixture
def manager():
    return PermissionManager()

def test_permission_decision_properties():
    # Baseline checks
    req = PermissionRequest(capability_id="com.nova.hello", scope=PermissionScope.OS_FILES_READ)
    assert req.capability_id == "com.nova.hello"

@pytest.mark.asyncio
async def test_baseline_policy_denial(manager):
    # com.nova.hello is ONLY allowed OS_FILES_READ.
    req = PermissionRequest(capability_id="com.nova.hello", scope=PermissionScope.OS_FILES_WRITE)
    result = await manager.evaluate(req)
    
    assert result.decision == PermissionDecision.DENY
    assert result.is_allowed is False
    assert "Policy Reject" in result.message

@pytest.mark.asyncio
async def test_prompt_for_unauthorized_scope(manager):
    # Allowed by baseline policy, but no explicit grant exists yet.
    req = PermissionRequest(capability_id="com.nova.hello", scope=PermissionScope.OS_FILES_READ)
    result = await manager.evaluate(req)
    
    assert result.decision == PermissionDecision.PROMPT
    assert result.is_allowed is False

@pytest.mark.asyncio
async def test_grant_and_allow(manager):
    req = PermissionRequest(capability_id="com.nova.hello", scope=PermissionScope.OS_FILES_READ)
    
    await manager.grant("com.nova.hello", PermissionScope.OS_FILES_READ)
    result = await manager.evaluate(req)
    
    assert result.decision == PermissionDecision.ALLOW
    assert result.is_allowed is True

@pytest.mark.asyncio
async def test_revoke(manager):
    req = PermissionRequest(capability_id="com.nova.hello", scope=PermissionScope.OS_FILES_READ)
    
    await manager.grant("com.nova.hello", PermissionScope.OS_FILES_READ)
    await manager.revoke("com.nova.hello", PermissionScope.OS_FILES_READ)
    
    result = await manager.evaluate(req)
    assert result.decision == PermissionDecision.PROMPT
    assert result.is_allowed is False

@pytest.mark.asyncio
async def test_temporary_grant_expiration(manager):
    req = PermissionRequest(capability_id="com.nova.hello", scope=PermissionScope.OS_FILES_READ)
    
    # Expired 1 hour ago
    expired_time = datetime.now(timezone.utc) - timedelta(hours=1)
    
    await manager.grant("com.nova.hello", PermissionScope.OS_FILES_READ, expires_at=expired_time)
    
    result = await manager.evaluate(req)
    assert result.decision == PermissionDecision.DENY
    assert result.is_allowed is False
    assert "expired" in result.message
