import asyncio
import os
import sys

# Add the root directory to path so we can import Benchmarks directly
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '01_Source')))

from Benchmarks.qualifier import QualificationRunner
from Benchmarks.dashboard import EngineeringDashboard

async def main():
    print("--- Starting Runtime Qualification ---")
    
    runner = QualificationRunner()
    
    print("\n[Executing Tier 4 - Certification Run]")
    success_4 = await runner.run_tier(4)
    
    if not success_4:
        print("\n[Tier 4 Failed - Halting]")
        
    dash = EngineeringDashboard()
    dash.generate()

if __name__ == "__main__":
    asyncio.run(main())
