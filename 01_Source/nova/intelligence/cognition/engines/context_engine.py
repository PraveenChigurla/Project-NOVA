"""
Context Engine.
Captures temporal and environmental variables.
"""
import time
import datetime
import logging
from nova.intelligence.cognition.models import ContextSnapshot

logger = logging.getLogger(__name__)

class ContextEngine:
    """Builds a temporal and locational snapshot of the current environment."""
    
    def capture(self) -> ContextSnapshot:
        logger.debug("ContextEngine capturing environment snapshot.")
        now = datetime.datetime.now()
        
        # Simple extraction for demo purposes
        day_of_week = now.strftime("%A")
        
        snapshot = ContextSnapshot(
            timestamp=time.time(),
            iso_date=now.isoformat(),
            day_of_week=day_of_week,
            hour=now.hour,
            timezone=time.tzname[0]
        )
        
        logger.info(f"Captured Context: {day_of_week}, Hour: {now.hour}")
        return snapshot
