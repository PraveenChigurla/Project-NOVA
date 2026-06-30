# NOVA CLI Guide

The NOVA CLI is the primary way to interact with the Cognitive Core. It replaces scattered demo scripts with a unified, interactive shell.

## Starting the CLI
To launch the interactive environment, open your terminal and type:
```bash
python nova.py
```

## Reserved Commands
Reserved commands always start with a forward slash (`/`). They are intercepted by the Presentation Layer and never reach the AI.

*   `/help` - Displays available commands.
*   `/clear` - Clears the terminal screen.
*   `/history` - Shows your command history for the session.
*   `/doctor` - Runs a diagnostic check on the Runtime, EventBus, and Registries.
*   `/version` - Displays the current platform version and certification status.
*   `/config` - Displays the active execution mode and memory paths.
*   `/benchmark [name]` - Runs an EVP endurance benchmark.

## Natural Language Control
Any input that does not start with a `/` is treated as a natural language command and passed to the NOVA Runtime.

**Examples:**
*   `> open chrome`
*   `> search github for project nova`
*   `> summarize the latest errors in the log file`

## Graceful Exit
To exit the CLI, type `/exit`, `quit`, or press `Ctrl+C`.
