# NOVA Daily Usage Guide

The ultimate goal of NOVA Version 1.0 is to minimize the amount of time you spend reaching for the keyboard and mouse for repetitive desktop interactions.

## The Daily Driver Workflow

### 1. Booting the Environment
You have two primary ways to interact with NOVA:
*   **Active Terminal:** Keep a terminal window open running `python nova.py`. This is ideal for development or when you need to closely monitor execution logs.
*   **Background Mode:** Run the System Tray Application (`python 01_Source/nova/tray/app.py`) or the Daemon (`python 01_Source/nova/daemon/hotkey.py`). This allows NOVA to hide in the background until summoned via `Ctrl+Alt+Space`.

### 2. Seamless Capabilities
NOVA comes pre-loaded with several standard Providers. You do not need to configure them to use them.

**Browser Control:**
*   `open chrome`
*   `go to github.com`
*   `click the login button`
*   `scroll down`

**System Interaction:**
*   `open vscode`
*   `close spotify`
*   `switch to whatsapp`
*   `type hello world`

### 3. Expanding NOVA (SDK)
When you encounter a workflow that NOVA does not understand, do not modify the core runtime. Use the NOVA SDK to build a new `.nova` package.

1.  Use the CLI to scaffold a skill: `python -m nova.sdk.cli new skill "my_custom_task"`
2.  Implement the logic within the bounds of the Capability Contracts.
3.  Package and load it into your local registry.

NOVA will dynamically ingest the new skill, and you can immediately begin using natural language to trigger it.
