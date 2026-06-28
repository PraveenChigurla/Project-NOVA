import asyncio
import logging
import sys

from nova.core.config import NovaConfig
from nova.core.logging import configure_logging
from nova.core.kernel import NovaKernel

logger = logging.getLogger("nova.main")

async def async_main() -> None:
    """Async entrypoint for the NOVA Kernel."""
    config = NovaConfig()
    configure_logging(config.get_log_level())
    
    logger.info("Initializing Project NOVA...", extra={"version": "0.1.0", "env": config.environment})
    
    kernel = NovaKernel(config)
    try:
        await kernel.boot()
        await kernel.run()
    except asyncio.CancelledError:
        logger.info("Main loop cancelled")
    except Exception as e:
        logger.critical(f"Unhandled exception in main: {e}", exc_info=True)
        sys.exit(1)

def main() -> None:
    """Synchronous entrypoint."""
    try:
        # Use Windows ProactorEventLoop if on windows and required for subprocesses later
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
            
        asyncio.run(async_main())
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting.")
        sys.exit(0)

if __name__ == "__main__":
    main()
