# NOVA Quick Start

Welcome to Project NOVA. 

NOVA is a governance-first computing architecture designed to act as an operating companion on your desktop. This guide will help you launch NOVA for the first time.

## 1. Prerequisites
Ensure you have Python 3.12+ installed and your dependencies are met.
```bash
pip install -r requirements.txt
```

## 2. Launching NOVA
NOVA exposes a unified command-line interface. To begin:
```bash
python nova.py
```

You will be greeted by the `NOVA >` prompt.

## 3. Verify System Health
Before trusting the Runtime with a task, ensure the architecture is fully loaded and stable.
```bash
NOVA > /doctor
```
This will run a diagnostic on the Capability Registry, Event Bus, Memory Subsystem, and Providers. If all report `[PASS]`, you are ready.

## 4. Your First Command
NOVA understands natural language. Start with something simple:
```bash
NOVA > open chrome
```
NOVA will compile this intent, route it to the Execution Engine, invoke the `BrowserProvider`, and execute the action seamlessly.

## 5. Background Mode
If you prefer not to keep a terminal window active, you can run the NOVA Daemon:
```bash
python 01_Source/nova/daemon/hotkey.py
```
This runs silently. Press `Ctrl+Alt+Space` from anywhere on your system to summon the interface.
