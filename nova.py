#!/usr/bin/env python3
"""
Project NOVA - Main Entry Point
"""
import sys
import os

# Ensure the 01_Source directory is in the path
current_dir = os.path.dirname(os.path.abspath(__file__))
source_dir = os.path.join(current_dir, "01_Source")
if source_dir not in sys.path:
    sys.path.insert(0, source_dir)

from nova.cli.shell import NovaShell

def main():
    if len(sys.argv) > 1:
        # User passed a direct command, e.g. `nova doctor`
        command = " ".join(sys.argv[1:])
        from nova.cli.router import CommandRouter
        router = CommandRouter()
        
        # Prepend slash for reserved commands if they typed "doctor" instead of "/doctor"
        if command in ["doctor", "version", "config", "benchmark"]:
            command = f"/{command}"
            
        router.route(command)
    else:
        # Launch the interactive shell
        shell = NovaShell()
        shell.start()

if __name__ == "__main__":
    main()
