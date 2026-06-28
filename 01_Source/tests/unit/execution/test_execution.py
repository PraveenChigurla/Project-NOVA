"""
Tests for the Execution Engine.
"""

import pytest
import asyncio
from typing import Dict, Any

from nova.intelligence.planning.models import ExecutionPlan, PlanStep, ExecutionStrategy, RetryPolicy
from nova.capabilities.registry import CapabilityRegistry
from nova.security.permissions import PermissionManager, PermissionScope
from nova.execution.engine import ExecutionEngine
from nova.execution.models import SessionState
from nova.capabilities.base import CapabilityMetadata, Capability
from nova.capabilities.hello_capability import HelloCapability

@pytest.fixture
def permission_manager():
    return PermissionManager()

@pytest.fixture
def capability_registry():
    return CapabilityRegistry()

@pytest.fixture
def execution_engine(capability_registry, permission_manager):
    return ExecutionEngine(capability_registry, permission_manager)

@pytest.mark.asyncio
async def test_successful_execution(execution_engine, capability_registry, permission_manager):
    # Setup capability
    meta = CapabilityMetadata(id="com.nova.hello", name="Hello", version="1.0", description="", supported_intents=["say_hello"])
    cap = HelloCapability(meta, permission_manager)
    await capability_registry.register(cap)
    await cap.system_initialize({})
    await cap.system_start()
    
    # Generate Plan
    step = PlanStep(
        step_id="1",
        capability_id="com.nova.hello",
        action="say_hello",
        parameters={"name": "Test"}
    )
    plan = ExecutionPlan(intent="test", strategy=ExecutionStrategy.SEQUENTIAL, steps=[step])
    
    # Execute
    result = await execution_engine.execute_plan(plan)
    
    assert result.success is True
    assert result.state == SessionState.COMPLETED
    assert len(result.step_results) == 1
    assert result.step_results[0].success is True
    assert result.step_results[0].data["message"] == "Hello, Test!"

@pytest.mark.asyncio
async def test_permission_denial(execution_engine, capability_registry, permission_manager):
    meta = CapabilityMetadata(id="com.nova.hello", name="Hello", version="1.0", description="", supported_intents=["read_file"])
    cap = HelloCapability(meta, permission_manager)
    await capability_registry.register(cap)
    await cap.system_initialize({})
    await cap.system_start()
    
    step = PlanStep(
        step_id="1",
        capability_id="com.nova.hello",
        action="read_file",
        parameters={"path": "C:/test.txt"}
    )
    plan = ExecutionPlan(intent="test", strategy=ExecutionStrategy.SEQUENTIAL, steps=[step])
    
    # We do NOT grant permission. It should fail.
    result = await execution_engine.execute_plan(plan)
    
    assert result.success is False
    assert result.state == SessionState.ROLLED_BACK # Fails, then rolls back
    assert result.step_results[0].success is False
    assert "Permission Framework blocked execution" in result.step_results[0].error

@pytest.mark.asyncio
async def test_retry_manager_triggers_on_failure(execution_engine, capability_registry, permission_manager):
    meta = CapabilityMetadata(id="com.nova.hello", name="Hello", version="1.0", description="", supported_intents=["cause_error"])
    cap = HelloCapability(meta, permission_manager)
    await capability_registry.register(cap)
    await cap.system_initialize({})
    await cap.system_start()
    
    step = PlanStep(
        step_id="1",
        capability_id="com.nova.hello",
        action="cause_error",
        retry_policy=RetryPolicy(max_retries=1, backoff_ms=10) # 1 retry, fast backoff
    )
    plan = ExecutionPlan(intent="test", strategy=ExecutionStrategy.SEQUENTIAL, steps=[step])
    
    result = await execution_engine.execute_plan(plan)
    
    assert result.success is False
    assert result.step_results[0].success is False
    # It should have attempted it twice (initial + 1 retry) and still failed.
    # The step result error will contain the capability crash message.
    assert "simulated capability crash" in result.step_results[0].error
