"""
NOVA Interactive Shell
"""
import sys
import os
from nova.cli.router import CommandRouter

class NovaShell:
    def __init__(self):
        self.router = CommandRouter()

    def start(self):
        print("=" * 50)
        print(" NOVA v1.0")
        print(" Good Evening, Praveen.")
        print(" Type /help for commands or just natural language.")
        print("=" * 50)
        
        while True:
            try:
                # Basic colored prompt
                user_input = input("\n\033[94m>\033[0m ")
                
                if user_input.strip() == "/clear":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    continue
                
                if user_input.strip() in ['exit', 'quit', '/quit', '/exit']:
                    self.stop()
                    break
                    
                self.router.route(user_input)
                
            except KeyboardInterrupt:
                # Graceful Ctrl+C
                print("\nType 'exit' to quit, or just keep going.")
            except EOFError:
                self.stop()
                break
            except Exception as e:
                print(f"\n\033[91m[Error]\033[0m {e}")

    def stop(self):
        print("\nGoodbye.")
        sys.exit(0)

if __name__ == "__main__":
    shell = NovaShell()
    shell.start()
