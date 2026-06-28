"""
Windows Desktop Provider.
Provides safe, native communication with the Windows OS via subprocess and ctypes.
"""

from typing import Dict, Any, Optional, List
import logging
import subprocess
import asyncio
import ctypes
import os

from nova.providers.base import (
    Provider,
    ProviderRequest,
    ProviderContext,
    ProviderError
)

logger = logging.getLogger(__name__)

class WindowsDesktopProvider(Provider):
    """
    Executes raw OS operations safely.
    Strictly forbids direct Win32 API calls from capabilities.
    """
    
    async def initialize(self) -> None:
        logger.info(f"[{self.metadata.id}] Initializing Windows Desktop Provider...")
        if os.name != 'nt':
            raise OSError("WindowsDesktopProvider requires a Windows operating system.")
        
    async def start(self) -> None:
        logger.info(f"[{self.metadata.id}] Desktop Provider Online.")
        
    async def execute(self, request: ProviderRequest, context: Optional[ProviderContext] = None) -> Dict[str, Any]:
        """Route the requested action to the correct subsystem."""
        logger.info(f"[{self.metadata.id}] Executing native action: {request.action}")
        
        # ---------------------------------------------------------
        # Process Operations
        # ---------------------------------------------------------
        if request.action == "launch_process":
            return await self._launch_process(request.payload.get("executable"))
            
        elif request.action == "terminate_process":
            return await self._terminate_process(request.payload.get("process_name"))
            
        elif request.action == "is_process_running":
            return await self._is_process_running(request.payload.get("process_name"))
            
        elif request.action == "list_processes":
            return await self._list_processes()
            
        # ---------------------------------------------------------
        # Window Operations
        # ---------------------------------------------------------
        elif request.action == "get_active_window":
            return await self._get_active_window()
            
        elif request.action == "get_window_bounds":
            return await self._get_window_bounds()
            
        # ---------------------------------------------------------
        # System Operations
        # ---------------------------------------------------------
        elif request.action == "screen_resolution":
            return await self._screen_resolution()
            
        elif request.action == "cursor_position":
            return await self._cursor_position()
            
        raise ValueError(f"WindowsDesktopProvider does not support action: '{request.action}'")

    async def stop(self) -> None:
        logger.info(f"[{self.metadata.id}] Desktop Provider Offline.")
        
    async def shutdown(self) -> None:
        logger.info(f"[{self.metadata.id}] Shutting down.")

    # =========================================================================
    # PROCESS IMPLEMENTATIONS (subprocess)
    # =========================================================================

    async def _launch_process(self, executable: Optional[str]) -> Dict[str, Any]:
        if not executable:
            raise ValueError("Missing 'executable' parameter.")
            
        try:
            # We use start so it detaches from our python process tree slightly
            # and we don't block. Wait, subprocess.Popen works.
            # We must be careful not to block.
            logger.debug(f"Spawning process: {executable}")
            process = subprocess.Popen(executable, shell=True)
            return {"status": "launched", "pid": process.pid}
        except Exception as e:
            raise RuntimeError(f"Failed to launch '{executable}': {e}")

    async def _terminate_process(self, process_name: Optional[str]) -> Dict[str, Any]:
        if not process_name:
            raise ValueError("Missing 'process_name' parameter.")
        try:
            # Taskkill is native windows
            subprocess.run(["taskkill", "/F", "/IM", process_name], check=True, capture_output=True)
            return {"status": "terminated"}
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to terminate '{process_name}': {e.stderr.decode()}")

    async def _is_process_running(self, process_name: Optional[str]) -> Dict[str, Any]:
        if not process_name:
            raise ValueError("Missing 'process_name' parameter.")
        try:
            output = subprocess.check_output(f'tasklist /FI "IMAGENAME eq {process_name}"', shell=True).decode()
            is_running = process_name.lower() in output.lower()
            return {"is_running": is_running}
        except Exception as e:
            raise RuntimeError(f"Failed to query process '{process_name}': {e}")

    async def _list_processes(self) -> Dict[str, Any]:
        try:
            output = subprocess.check_output('tasklist /FO CSV /NH', shell=True).decode()
            processes = []
            for line in output.strip().split('\n'):
                parts = line.split('","')
                if len(parts) >= 1:
                    processes.append(parts[0].strip('"'))
            # Filter out duplicates and empty
            processes = list(set([p for p in processes if p]))
            return {"processes": processes}
        except Exception as e:
            raise RuntimeError(f"Failed to list processes: {e}")

    # =========================================================================
    # WINDOW / SYSTEM IMPLEMENTATIONS (ctypes)
    # =========================================================================

    async def _get_active_window(self) -> Dict[str, Any]:
        try:
            user32 = ctypes.windll.user32
            hwnd = user32.GetForegroundWindow()
            length = user32.GetWindowTextLengthW(hwnd)
            buf = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buf, length + 1)
            return {"title": buf.value, "hwnd": hwnd}
        except Exception as e:
            raise RuntimeError(f"Failed to get active window: {e}")

    async def _get_window_bounds(self) -> Dict[str, Any]:
        try:
            user32 = ctypes.windll.user32
            hwnd = user32.GetForegroundWindow()
            rect = ctypes.wintypes.RECT()
            user32.GetWindowRect(hwnd, ctypes.pointer(rect))
            return {
                "left": rect.left,
                "top": rect.top,
                "right": rect.right,
                "bottom": rect.bottom,
                "width": rect.right - rect.left,
                "height": rect.bottom - rect.top
            }
        except Exception as e:
            raise RuntimeError(f"Failed to get window bounds: {e}")

    async def _screen_resolution(self) -> Dict[str, Any]:
        try:
            user32 = ctypes.windll.user32
            width = user32.GetSystemMetrics(0)
            height = user32.GetSystemMetrics(1)
            return {"width": width, "height": height}
        except Exception as e:
            raise RuntimeError(f"Failed to get screen resolution: {e}")

    async def _cursor_position(self) -> Dict[str, Any]:
        try:
            class POINT(ctypes.Structure):
                _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
            
            pt = POINT()
            ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
            return {"x": pt.x, "y": pt.y}
        except Exception as e:
            raise RuntimeError(f"Failed to get cursor position: {e}")
