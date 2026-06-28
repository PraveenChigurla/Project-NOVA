"""
End-to-End Integration Tests for NOVA Pipeline.
"""

import pytest
import os
import asyncio
from nova.core.config import NovaConfig
from nova.core.kernel import NovaKernel
from nova.security.permissions.models import PermissionScope

@pytest.fixture
async def kernel():
    config = NovaConfig()
    k = NovaKernel(config)
    await k.boot()
    yield k
    await k.shutdown()

@pytest.mark.asyncio
async def test_e2e_unknown_intent(kernel):
    # Scenario 4: Unknown Intent
    res = await kernel.execute_command("Cook dinner")
    assert res is None # Pipeline aborts early

@pytest.mark.asyncio
async def test_e2e_permission_denied(kernel):
    # Scenario 3: Permission Denied
    if os.name != 'nt':
        pytest.skip("Windows only")
        
    res = await kernel.execute_command("Open Notepad")
    assert res is not None
    assert res.success is False
    assert len(res.step_results) == 1
    assert res.step_results[0].success is False
    assert "Permission" in res.step_results[0].error

@pytest.mark.asyncio
async def test_e2e_capability_failure(kernel):
    # Scenario 5: Capability Failure
    if os.name != 'nt':
        pytest.skip("Windows only")
        
    await kernel.permission_manager.grant("com.nova.desktop.process", PermissionScope.OS_PROCESS_START)
    
    res = await kernel.execute_command("Launch fake_app")
    assert res is not None
    assert res.success is False
    assert len(res.step_results) == 1
    assert res.step_results[0].success is False
    assert "Failed to launch" in res.step_results[0].error
