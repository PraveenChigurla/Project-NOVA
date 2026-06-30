"""
NOVA System Tray Application
"""
import sys
import threading
import time

try:
    import pystray
    from pystray import MenuItem as item
    from PIL import Image, ImageDraw
    _TRAY_AVAILABLE = True
except ImportError:
    _TRAY_AVAILABLE = False

def create_image(width, height, color1, color2):
    """Generate a simple square icon."""
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 4, height // 4, width * 3 // 4, height * 3 // 4),
        fill=color2)
    return image

class NovaTrayApp:
    def __init__(self):
        self.icon = None
        
    def start_nova(self, icon, item):
        print("[Tray] Starting NOVA Runtime...")
        
    def stop_nova(self, icon, item):
        print("[Tray] Stopping NOVA Runtime...")
        
    def show_logs(self, icon, item):
        print("[Tray] Opening logs...")
        
    def exit_action(self, icon, item):
        icon.stop()
        
    def run(self):
        if not _TRAY_AVAILABLE:
            print("[Warning] 'pystray' or 'Pillow' not installed. Tray app disabled.")
            return
            
        menu = (
            item('Start NOVA', self.start_nova),
            item('Stop NOVA', self.stop_nova),
            item('View Logs', self.show_logs),
            item('Exit', self.exit_action)
        )
        
        # Blue/Cyan icon for NOVA
        image = create_image(64, 64, 'black', 'cyan')
        self.icon = pystray.Icon("NOVA", image, "Project NOVA", menu)
        print("NOVA System Tray initialized.")
        self.icon.run()

if __name__ == "__main__":
    app = NovaTrayApp()
    app.run()
