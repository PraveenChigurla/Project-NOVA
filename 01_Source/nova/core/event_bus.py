import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Callable, Awaitable, Any

logger = logging.getLogger(__name__)

class IEventBus(ABC):
    @abstractmethod
    async def publish(self, topic: str, payload: Any) -> None:
        pass

    @abstractmethod
    def subscribe(self, topic: str, callback: Callable[[Any], Awaitable[None]]) -> None:
        pass

class AsyncioEventBus(IEventBus):
    """
    In-memory asynchronous event bus using asyncio primitives.
    """
    def __init__(self, max_queue_size: int = 1000):
        self._subscribers: Dict[str, List[Callable[[Any], Awaitable[None]]]] = {}
        self._queue: asyncio.Queue = asyncio.Queue(maxsize=max_queue_size)
        self._dispatch_task: asyncio.Task | None = None
        self._running = False

    def subscribe(self, topic: str, callback: Callable[[Any], Awaitable[None]]) -> None:
        if topic not in self._subscribers:
            self._subscribers[topic] = []
        self._subscribers[topic].append(callback)
        logger.debug(f"Subscribed to topic: {topic}")

    async def publish(self, topic: str, payload: Any) -> None:
        if not self._running:
            logger.warning(f"EventBus is not running. Dropping message for topic: {topic}")
            return
            
        try:
            await self._queue.put((topic, payload))
            logger.debug(f"Published to topic: {topic}")
        except asyncio.QueueFull:
            logger.error(f"EventBus queue is full. Dropping message for topic: {topic}")

    async def start(self) -> None:
        """Starts the background dispatch loop."""
        self._running = True
        self._dispatch_task = asyncio.create_task(self._dispatch_loop(), name="EventBus-Dispatch")
        logger.info("EventBus started")

    async def stop(self) -> None:
        """Stops the event bus and flushes the queue."""
        self._running = False
        if self._dispatch_task:
            self._dispatch_task.cancel()
            try:
                await self._dispatch_task
            except asyncio.CancelledError:
                pass
        logger.info("EventBus stopped")

    async def _dispatch_loop(self) -> None:
        try:
            while self._running:
                topic, payload = await self._queue.get()
                subscribers = self._subscribers.get(topic, [])
                
                for callback in subscribers:
                    try:
                        await callback(payload)
                    except Exception as e:
                        logger.error(f"Error in subscriber for topic {topic}: {e}", exc_info=True)
                        
                self._queue.task_done()
        except asyncio.CancelledError:
            logger.debug("EventBus dispatch loop cancelled")
            raise
