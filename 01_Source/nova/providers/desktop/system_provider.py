"""
NOVA System Provider
Abstracts OS-specific application and system controls.
"""
import os
import platform
import subprocess
import psutil

class SystemProvider:
    def __init__(self):
        self.os_type = platform.system().lower()

    def launch_application(self, executables: list) -> bool:
        """Launches the first valid executable in the list for the current OS."""
        for exe in executables:
            try:
                # Check if it's already running
                exe_basename = os.path.basename(exe).lower()
                for proc in psutil.process_iter(['name']):
                    if proc.info['name'] and proc.info['name'].lower() == exe_basename:
                        print(f"[{self.os_type.capitalize()}] Application '{exe_basename}' is already running. Focusing...")
                        # Focus logic goes here (pygetwindow / ctypes)
                        return True

                print(f"[{self.os_type.capitalize()}] Launching {exe}...")
                if self.os_type == 'windows':
                    # Use start so it detaches
                    subprocess.Popen(f"start \"\" \"{exe}\"", shell=True)
                elif self.os_type == 'darwin':
                    subprocess.Popen(["open", "-a", exe])
                else:
                    subprocess.Popen([exe])
                return True
            except Exception as e:
                print(f"[{self.os_type.capitalize()}] Failed to launch {exe}: {e}")
        return False

    def close_application(self, executables: list) -> bool:
        """Kills the process."""
        killed = False
        for exe in executables:
            exe_basename = os.path.basename(exe).lower()
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] and proc.info['name'].lower() == exe_basename:
                    try:
                        print(f"[{self.os_type.capitalize()}] Terminating {exe_basename}...")
                        proc.terminate()
                        killed = True
                    except:
                        pass
        return killed

    def shutdown_system(self):
        """OS-agnostic shutdown."""
        print(f"[{self.os_type.capitalize()}] Executing system shutdown...")
        if self.os_type == 'windows':
            subprocess.run(["shutdown", "/s", "/t", "1"])
        elif self.os_type == 'darwin':
             subprocess.run(["osascript", "-e", 'tell app "System Events" to shut down'])
        else:
             subprocess.run(["shutdown", "-h", "now"])
