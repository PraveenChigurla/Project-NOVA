"""
State Engine.
Constructs the WorldState by querying the underlying OS.
"""
import logging
import psutil
from nova.intelligence.cognition.models import WorldState

logger = logging.getLogger(__name__)

class StateEngine:
    """Scans the physical OS to determine active applications."""
    
    def capture(self) -> WorldState:
        logger.debug("StateEngine capturing WorldState...")
        active_procs = []
        
        # Iterate over all running process names
        # Note: on some OS's this requires elevated permissions, but basic querying usually works for user space apps.
        for proc in psutil.process_iter(['name']):
            try:
                name = proc.info.get('name')
                if name:
                    active_procs.append(name.lower())
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
                
        # Deduplicate list
        active_procs = list(set(active_procs))
        
        state = WorldState(active_processes=active_procs)
        
        # Quick log of common apps
        if state.is_process_running("chrome") or state.is_process_running("msedge"):
            logger.info("Detected Browser running.")
        if state.is_process_running("code") or state.is_process_running("devenv"):
            logger.info("Detected IDE running.")
            
        return state
