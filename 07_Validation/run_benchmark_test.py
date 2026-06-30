import asyncio
import os
import sys

# Add the root directory to path so we can import benchmarks directly
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '01_Source')))

from Benchmarks.harness import BenchmarkRunner
from Benchmarks.replay import DeterministicReplay

async def main():
    print("--- Starting EVP Benchmark Harness Validation ---")
    
    # Run 1: Clean small execution
    config_clean = {
        "iterations": 100,
        "warmup": 10,
        "inject_failure": False,
        "seed": "CLEAN_TEST"
    }
    
    runner1 = BenchmarkRunner(config_clean)
    await runner1.run()
    
    print("\n--- Starting Failure Injection Validation ---")
    # Run 2: Inject failure to test deterministic replay capture
    config_fail = {
        "iterations": 50,
        "warmup": 5,
        "inject_failure": True,
        "fail_at": 25,
        "seed": "FAIL_TEST"
    }
    
    runner2 = BenchmarkRunner(config_fail)
    await runner2.run()
    
    print("\n--- Starting Deterministic Replay Validation ---")
    # Run 3: Test Replay
    replay = DeterministicReplay()
    plan = replay.replay("07_Validation/Benchmarks/failure_000025.json")
    print(f"Reconstructed Plan ID: {plan.plan_id}")
    print(f"Steps in plan: {len(plan.steps)}")
    
if __name__ == "__main__":
    asyncio.run(main())
