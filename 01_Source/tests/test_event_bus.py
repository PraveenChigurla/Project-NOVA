import pytest
import asyncio
from nova.core.event_bus import AsyncioEventBus

@pytest.mark.asyncio
async def test_event_bus_publish_subscribe():
    bus = AsyncioEventBus()
    
    received_payloads = []
    
    async def dummy_callback(payload):
        received_payloads.append(payload)
        
    bus.subscribe("Test.Event", dummy_callback)
    
    # Start the bus
    await bus.start()
    
    # Publish an event
    await bus.publish("Test.Event", {"data": 123})
    
    # Allow event loop to process queue
    await asyncio.sleep(0.1)
    
    # Stop the bus
    await bus.stop()
    
    assert len(received_payloads) == 1
    assert received_payloads[0] == {"data": 123}

@pytest.mark.asyncio
async def test_event_bus_dropped_when_not_running():
    bus = AsyncioEventBus()
    
    received_payloads = []
    
    async def dummy_callback(payload):
        received_payloads.append(payload)
        
    bus.subscribe("Test.Event", dummy_callback)
    
    # Do NOT start the bus
    await bus.publish("Test.Event", {"data": 123})
    
    assert len(received_payloads) == 0
