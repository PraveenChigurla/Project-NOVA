"""
NOVA Global Hotkey Daemon
"""
import sys
import threading

try:
    import keyboard
    _KEYBOARD_AVAILABLE = True
except ImportError:
    _KEYBOARD_AVAILABLE = False

def on_hotkey():
    """Triggered when Ctrl+Alt+Space is pressed."""
    print("\n[NOVA Daemon] Hotkey detected. Launching NOVA interface...")
    # In full integration, this would spawn a tkinter/PyQt popup window.
    # For now, it delegates back to the CLI shell if running, or spawns one.
    import os
    if os.name == 'nt':
        os.system("start python nova.py")
    else:
        # Simplistic fallback for mac/linux terminals
        os.system("python3 nova.py")

class NovaDaemon:
    def __init__(self):
        self.running = False
        
    def start(self):
        if not _KEYBOARD_AVAILABLE:
            print("[Warning] 'keyboard' module not installed. Hotkeys disabled.")
            print("Run 'pip install keyboard' to enable global hotkeys.")
            return
            
        print("Starting NOVA background daemon... (Press Ctrl+Alt+Space to summon)")
        keyboard.add_hotkey('ctrl+alt+space', on_hotkey)
        self.running = True
        
        # Keep daemon alive
        keyboard.wait()

    def stop(self):
        self.running = False

if __name__ == "__main__":
    daemon = NovaDaemon()
    daemon.start()
