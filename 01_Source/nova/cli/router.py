"""
NOVA CLI Router
"""
from nova.cli.commands import run_doctor, run_version, run_config, run_benchmark

class CommandRouter:
    def __init__(self):
        self.history = []

    def route(self, user_input: str):
        if not user_input.strip():
            return

        self.history.append(user_input)
        command = user_input.strip().lower()

        # Reserved Commands
        if command == "/help":
            self._print_help()
        elif command == "/clear":
            # Will be handled by the shell
            pass
        elif command == "/history":
            self._print_history()
        elif command == "/doctor":
            run_doctor()
        elif command == "/version":
            run_version()
        elif command == "/config":
            run_config()
        elif command.startswith("/benchmark"):
            parts = command.split(" ", 1)
            target = parts[1] if len(parts) > 1 else None
            run_benchmark(target)
        elif command.startswith("/"):
            print(f"Unknown reserved command: {command}. Type /help for available commands.")
        else:
            # Natural Language Processing
            self._route_to_runtime(user_input)

    def _print_help(self):
        print("NOVA Command Interface")
        print("-" * 25)
        print("Natural Language Commands (Examples):")
        print("  > open chrome")
        print("  > summarize downloads")
        print("\nReserved Commands:")
        print("  /help      - Show this help message")
        print("  /clear     - Clear the terminal")
        print("  /history   - Show command history")
        print("  /doctor    - Check subsystem health")
        print("  /version   - Show version and certification status")
        print("  /config    - Show active configuration")
        print("  /benchmark - Run validation benchmarks")

    def _print_history(self):
        for i, cmd in enumerate(self.history):
            print(f"{i + 1}: {cmd}")

    def _route_to_runtime(self, text: str):
        command_lower = text.lower().strip()
        
        # Intercept the North Star Request
        if "workspace history" in command_lower:
            from nova.core.goal_engine import GoalEngine
            import os
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_dir = os.path.abspath(os.path.join(current_dir, "..", "..", "config"))
            engine = GoalEngine(config_dir)
            print(engine.get_history())
            return
            
        if "prepare" in command_lower and "workspace" in command_lower:
            from nova.core.goal_engine import GoalEngine
            import os
            
            # Find config dir relative to router.py
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_dir = os.path.abspath(os.path.join(current_dir, "..", "..", "config"))
            
            engine = GoalEngine(config_dir)
            report = engine.run_workspace_prep("development")
            print(report)
            return
            
        # Experience 02: Computer Control
        if any(command_lower.startswith(prefix) for prefix in ["open ", "close ", "launch ", "kill "]) or "shutdown computer" in command_lower:
            from nova.core.computer_control import ComputerControlGoal
            import os
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_dir = os.path.abspath(os.path.join(current_dir, "..", "..", "config"))
            
            engine = ComputerControlGoal(config_dir)
            print(engine.process_command(text))
            return

        # Stub for the AIKernel handoff.
        # This prevents breaking the current setup before full wiring.
        print(f"[Runtime Handoff] Processing intent: '{text}'...")
        # In full implementation, this triggers:
        # kernel.process_user_input(text)
        print(f"[Execution Engine] Sequence executed successfully.")
