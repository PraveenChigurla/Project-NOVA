import json
import os
from typing import Dict, Any

class EvidenceReporter:
    """
    Serializes benchmark metrics into JSON and Markdown certification reports.
    """
    def __init__(self, output_dir: str = "07_Validation/Benchmarks"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
    def generate_report(self, summary: Dict[str, Any], config: Dict[str, Any], title: str = "Milestone 1 - Runtime Stability"):
        
        # 1. Export JSON
        json_path = os.path.join(self.output_dir, "runtime_metrics.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump({
                "config": config,
                "metrics": summary
            }, f, indent=2)
            
        # 2. Determine Certification Pass/Fail
        passed = (
            summary.get("unexpected_failures", 1) == 0 and 
            summary.get("total_executions", 0) == config.get("iterations", 0)
        )
        
        # 3. Export Markdown
        md_path = os.path.join(self.output_dir, "runtime_benchmark.md")
        
        lines = [
            f"# Engineering Validation",
            f"## {title}",
            "",
            f"**Status:** {'✅ PASS' if passed else '❌ FAIL'}",
            "",
            "### Configuration",
            "```json",
            json.dumps(config, indent=2),
            "```",
            "",
            "### Metrics",
            "| Metric | Value |",
            "| :--- | :--- |",
            f"| Total Executions | {summary.get('total_executions')} |",
            f"| Successes | {summary.get('successes')} |",
            f"| Expected Failures | {summary.get('expected_failures')} |",
            f"| Unexpected Failures | {summary.get('unexpected_failures')} |",
            f"| Total Time | {summary.get('total_time_seconds'):.2f} s |",
            f"| Throughput | {summary.get('throughput_hz'):.2f} plans/sec |",
            f"| Avg Latency | {summary.get('latency_avg_ms'):.2f} ms |",
            f"| P95 Latency | {summary.get('latency_p95_ms'):.2f} ms |",
            f"| P99 Latency | {summary.get('latency_p99_ms'):.2f} ms |",
            f"| Peak Memory | {summary.get('peak_memory_mb'):.2f} MB |",
            ""
        ]
        
        if summary.get("checkpoints"):
            lines.extend([
                "### Telemetry Checkpoints",
                "| Iteration | Heap (MB) | Objects | Q Depth | P50 (ms) | P95 (ms) | P99 (ms) |",
                "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
            ])
            for cp in summary["checkpoints"]:
                it = cp["iteration"]
                heap = cp["telemetry"]["heap_size_mb"]
                obj = cp["telemetry"]["tracked_objects"]
                q = cp["telemetry"]["event_queue_depth"]
                p50 = cp["latency"]["p50_ms"]
                p95 = cp["latency"]["p95_ms"]
                p99 = cp["latency"]["p99_ms"]
                lines.append(f"| {it} | {heap:.2f} | {obj} | {q} | {p50:.2f} | {p95:.2f} | {p99:.2f} |")
            lines.append("")
        
        if not passed:
            lines.extend([
                "### Failure Analysis",
                "The benchmark failed to meet the certification criteria. Check the deterministic replay logs for details."
            ])
            
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
            
        return md_path
