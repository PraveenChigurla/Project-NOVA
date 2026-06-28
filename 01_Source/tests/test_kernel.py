import pytest
import asyncio
from nova.core.config import NovaConfig
from nova.core.kernel import NovaKernel
from nova.core.event_bus import IEventBus

@pytest.mark.asyncio
async def test_kernel_boot_and_shutdown():
    config = NovaConfig(log_level="DEBUG", event_bus_max_queue_size=10)
    kernel = NovaKernel(config)
    
    # Run boot sequence
    await kernel.boot()
    
    # Assert infrastructure was registered
    event_bus = kernel.locator.resolve(IEventBus)
    assert event_bus is not None
    
    # Run the kernel in the background
    run_task = asyncio.create_task(kernel.run())
    
    # Allow the loop to spin up
    await asyncio.sleep(0.1)
    
    # Request shutdown via event bus
    await event_bus.publish("System.Abort.Requested", {"reason": "Test Shutdown"})
    
    # Wait for graceful shutdown
    await run_task
    
    # Ensure it's not running anymore
    assert not kernel._is_running
