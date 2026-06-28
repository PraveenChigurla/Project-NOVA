"""
Cancellation Manager.
Provides an asyncio.Event token to pause or hard-cancel execution mid-flight.
"""

import asyncio
import logging

logger = logging.getLogger(__name__)

class ExecutionCancelledError(Exception):
    pass

class CancellationManager:
    """Manages cancellation and pause states for an execution session."""
    def __init__(self):
        self._cancel_event = asyncio.Event()
        self._pause_event = asyncio.Event()
        self._pause_event.set() # Set means "not paused" (can proceed)

    def cancel(self) -> None:
        """Trigger a hard cancellation."""
        logger.warning("Execution cancellation requested!")
        self._cancel_event.set()

    def pause(self) -> None:
        """Pause execution."""
        logger.info("Execution pause requested.")
        self._pause_event.clear()

    def resume(self) -> None:
        """Resume execution."""
        logger.info("Execution resume requested.")
        self._pause_event.set()

    async def check_state(self) -> None:
        """
        Check if we should cancel or pause.
        Call this before every step.
        """
        if self._cancel_event.is_set():
            raise ExecutionCancelledError("Execution was cancelled by the user or system.")
            
        if not self._pause_event.is_set():
            logger.info("Execution is paused. Waiting to resume...")
            await self._pause_event.wait()
            logger.info("Execution resumed.")
            
            # Re-check cancellation after waking up from pause
            if self._cancel_event.is_set():
                raise ExecutionCancelledError("Execution was cancelled during pause.")
