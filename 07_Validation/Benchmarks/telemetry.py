import gc
import psutil
import os
import tracemalloc
from typing import Dict, Any, List
from datetime import datetime
from pydantic import BaseModel

class ObservabilitySnapshot(BaseModel):
    iteration: int
    timestamp: str
    heap_size_mb: float
    tracked_objects: int
    gc_collections: Dict[int, int]
    event_queue_depth: int
    active_tasks: int

class TelemetryTracker:
    """
    Captures process-level and runtime-level metrics at specific checkpoints.
    """
    def __init__(self):
        self.process = psutil.Process(os.getpid())
        if not tracemalloc.is_tracing():
            tracemalloc.start()
            
    def capture_snapshot(self, iteration: int, event_queue_depth: int = 0, active_tasks: int = 0) -> ObservabilitySnapshot:
        mem_info = self.process.memory_info()
        heap_size_mb = round(mem_info.rss / (1024 * 1024), 2)
        
        # Python GC stats
        tracked_objects = len(gc.get_objects())
        gc_stats = gc.get_stats()
        collections = {
            0: gc_stats[0]['collections'],
            1: gc_stats[1]['collections'],
            2: gc_stats[2]['collections']
        }
        
        return ObservabilitySnapshot(
            iteration=iteration,
            timestamp=datetime.utcnow().isoformat() + "Z",
            heap_size_mb=heap_size_mb,
            tracked_objects=tracked_objects,
            gc_collections=collections,
            event_queue_depth=event_queue_depth,
            active_tasks=active_tasks
        )
