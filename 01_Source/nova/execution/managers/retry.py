"""
Retry Manager.
Intercepts step failures and applies backoff math based on RetryPolicy.
"""

import asyncio
import logging
from typing import Callable, Awaitable, Any

from nova.intelligence.planning.models import RetryPolicy
from nova.execution.managers.cancellation import CancellationManager

logger = logging.getLogger(__name__)

class RetryManager:
    """Manages retry logic and backoff for failed steps."""
    
    @staticmethod
    async def execute_with_retry(
        step_id: str,
        policy: RetryPolicy,
        cancellation: CancellationManager,
        func: Callable[[], Awaitable[Any]]
    ) -> Any:
        """
        Executes an async function, retrying upon failure according to the policy.
        """
        attempts = 0
        max_attempts = policy.max_retries + 1
        
        while attempts < max_attempts:
            await cancellation.check_state()
            try:
                return await func()
            except Exception as e:
                attempts += 1
                if attempts >= max_attempts:
                    logger.error(f"Step {step_id} failed after {attempts} attempts. Error: {e}")
                    raise
                    
                backoff_time = (policy.backoff_ms * (2 ** (attempts - 1))) / 1000.0
                logger.warning(f"Step {step_id} failed (attempt {attempts}/{max_attempts}). Retrying in {backoff_time}s... Error: {e}")
                
                # Check cancellation during backoff sleep
                try:
                    await asyncio.wait_for(cancellation._cancel_event.wait(), timeout=backoff_time)
                    # If we get here, cancellation was triggered
                    raise Exception("Execution cancelled during backoff.")
                except asyncio.TimeoutError:
                    # Normal backoff completed
                    pass
