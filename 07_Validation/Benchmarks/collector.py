import time
import tracemalloc
import gc
from typing import Dict, List, Any
import psutil
import os
import uuid
from .telemetry import ObservabilitySnapshot

class MetricsCollector:
    """
    Collects runtime metrics including latency, memory, and CPU usage.
    Supports tiered checkpoints.
    """
    def __init__(self, run_uuid: str = None):
        self.run_uuid = run_uuid or f"EVP-RUN-{time.strftime('%Y')}-{str(uuid.uuid4())[:6]}"
        self.latencies: List[float] = []
        self.start_time = 0.0
        self.end_time = 0.0
        self.success_count = 0
        self.expected_failure_count = 0
        self.unexpected_failure_count = 0
        
        self.peak_memory_mb = 0.0
        self.process = psutil.Process(os.getpid())
        
        # Checkpoints data
        self.checkpoints: List[Dict[str, Any]] = []
        self._last_checkpoint_idx = 0
        
    def start_run(self):
        if not tracemalloc.is_tracing():
            tracemalloc.start()
        gc.collect()
        self.start_time = time.perf_counter()
        self.update_memory()
        
    def record_execution(self, latency: float, success: bool, expected_failure: bool = False):
        self.latencies.append(latency)
        if success:
            self.success_count += 1
        elif expected_failure:
            self.expected_failure_count += 1
        else:
            self.unexpected_failure_count += 1
            
        if len(self.latencies) % 1000 == 0:
            self.update_memory()
            
    def update_memory(self):
        mem_info = self.process.memory_info()
        current_mb = mem_info.rss / (1024 * 1024)
        if current_mb > self.peak_memory_mb:
            self.peak_memory_mb = current_mb
            
    def record_checkpoint(self, snapshot: ObservabilitySnapshot):
        """Records a checkpoint segment for drift analysis."""
        idx = len(self.latencies)
        segment_latencies = self.latencies[self._last_checkpoint_idx:idx]
        self._last_checkpoint_idx = idx
        
        if not segment_latencies:
            return
            
        segment_latencies.sort()
        count = len(segment_latencies)
        
        checkpoint_data = {
            "iteration": snapshot.iteration,
            "telemetry": snapshot.model_dump(),
            "latency": {
                "p50_ms": segment_latencies[count // 2] * 1000,
                "p95_ms": segment_latencies[int(count * 0.95)] * 1000,
                "p99_ms": segment_latencies[int(count * 0.99)] * 1000
            }
        }
        self.checkpoints.append(checkpoint_data)
        
    def end_run(self):
        self.end_time = time.perf_counter()
        self.update_memory()
        
    def get_summary(self) -> Dict[str, Any]:
        self.latencies.sort()
        count = len(self.latencies)
        
        if count == 0:
            return {"run_uuid": self.run_uuid}
            
        return {
            "run_uuid": self.run_uuid,
            "total_executions": count,
            "successes": self.success_count,
            "expected_failures": self.expected_failure_count,
            "unexpected_failures": self.unexpected_failure_count,
            "total_time_seconds": self.end_time - self.start_time,
            "throughput_hz": count / (self.end_time - self.start_time) if self.end_time > self.start_time else 0,
            "latency_avg_ms": (sum(self.latencies) / count) * 1000,
            "latency_median_ms": self.latencies[count // 2] * 1000,
            "latency_p95_ms": self.latencies[int(count * 0.95)] * 1000,
            "latency_p99_ms": self.latencies[int(count * 0.99)] * 1000,
            "peak_memory_mb": self.peak_memory_mb,
            "checkpoints": self.checkpoints
        }
