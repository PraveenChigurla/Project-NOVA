"""
Computer Control Goal Engine
Handles intents to control applications and the operating system directly.
"""
import time
from nova.core.app_registry import AppRegistry

class ComputerControlGoal:
    def __init__(self, config_dir: str):
        self.registry = AppRegistry(config_dir)

    def process_command(self, text: str) -> str:
        """Parses simple NLP intents for Experience 02 and delegates execution."""
        text_lower = text.lower().strip()
        report = []
        
        # Determine Intent
        intent = "unknown"
        target_alias = ""
        
        if text_lower.startswith("open ") or text_lower.startswith("launch "):
            intent = "open"
            target_alias = text_lower.replace("open ", "").replace("launch ", "").strip()
        elif text_lower.startswith("close ") or text_lower.startswith("kill "):
            intent = "close"
            target_alias = text_lower.replace("close ", "").replace("kill ", "").strip()
            
        report.append(f"Goal: Computer Control ({intent.capitalize()} '{target_alias}')\n")
        
        if intent == "open":
            app_record = self.registry.resolve_alias(target_alias)
            if not app_record:
                report.append(f"✗ Unknown Application: '{target_alias}'")
                report.append("\n\033[93m[Interactive Learning]\033[0m")
                report.append(f"I don't know the alias '{target_alias}'.")
                report.append("Searching installed applications...")
                report.append(f"Type '/learn {target_alias} = <app_id>' to teach me.")
            else:
                from nova.providers.desktop.system_provider import SystemProvider
                provider = SystemProvider()
                
                report.append(f"✓ Resolved alias '{target_alias}' -> {app_record['id']}")
                success = provider.launch_application(app_record["executables"])
                
                if success:
                    report.append(f"✓ Launch successful.")
                else:
                    report.append(f"✗ Launch failed.")
                    
        elif intent == "close":
            app_record = self.registry.resolve_alias(target_alias)
            if not app_record:
                report.append(f"✗ Unknown Application: '{target_alias}'")
            else:
                from nova.providers.desktop.system_provider import SystemProvider
                provider = SystemProvider()
                
                report.append(f"✓ Resolved alias '{target_alias}' -> {app_record['id']}")
                success = provider.close_application(app_record["executables"])
                
                if success:
                    report.append(f"✓ Close successful.")
                else:
                    report.append(f"✗ Could not find running process to close.")
                    
        elif text_lower == "shutdown computer":
             report.append("\n\033[91m[Action Required]\033[0m")
             report.append("You have requested to SHUTDOWN the computer.")
             report.append("Are you sure? Type Y/N")
             
        else:
             report.append(f"✗ Unrecognized command structure for Computer Control.")
             
        return "\n".join(report)
