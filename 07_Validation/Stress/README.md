# Stress Testing

This directory contains scripts and results for testing the NOVA Runtime under continuous, heavy load.

**Key Tests:**
*   `100k_plan_execution.py`: Verifies long-running stability without memory leaks.
*   `event_bus_flood.py`: Tests the limits of the asynchronous event chronicle.
