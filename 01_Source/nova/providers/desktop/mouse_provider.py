"""
Mouse Provider.
Exposes low-level Win32 mouse primitives using pure ctypes.
"""
import ctypes
import time
import logging
from typing import Dict, Any, Optional, Tuple

from nova.providers.base import Provider, ProviderRequest, ProviderContext, ProviderMetadata, ProviderType

logger = logging.getLogger(__name__)

# --- Win32 API Constants ---
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
MOUSEEVENTF_WHEEL = 0x0800

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

class MouseProvider(Provider):
    """
    Low-level mouse controller. 
    Does not implement human-like timing; that is the Capability's job.
    """
    
    def __init__(self, metadata: ProviderMetadata):
        super().__init__(metadata)
        self._user32 = ctypes.windll.user32
        # Setup DPI awareness to ensure coordinates map correctly on modern Windows
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2) # PROCESS_PER_MONITOR_DPI_AWARE
        except AttributeError:
            self._user32.SetProcessDPIAware()
            
    async def initialize(self) -> None:
        logger.info(f"[{self.metadata.id}] Initializing Mouse Provider...")
        
    async def start(self) -> None:
        logger.info(f"[{self.metadata.id}] Mouse Provider Online.")
        
    async def execute(self, request: ProviderRequest, context: Optional[ProviderContext] = None) -> Dict[str, Any]:
        logger.debug(f"[{self.metadata.id}] Native Action: {request.action}")
        
        if request.action == "move_cursor":
            x = request.payload.get("x", 0)
            y = request.payload.get("y", 0)
            self._set_cursor_pos(x, y)
            return {"status": "moved", "x": x, "y": y}
            
        elif request.action == "click":
            button = request.payload.get("button", "left")
            self._click(button)
            return {"status": "clicked", "button": button}
            
        elif request.action == "get_position":
            x, y = self._get_cursor_pos()
            return {"x": x, "y": y}
            
        raise ValueError(f"MouseProvider does not support action: '{request.action}'")

    async def stop(self) -> None:
        pass
        
    async def shutdown(self) -> None:
        pass

    # =========================================================================
    # NATIVE CTYPES IMPLEMENTATIONS
    # =========================================================================

    def _set_cursor_pos(self, x: int, y: int):
        """Teleports the cursor natively."""
        self._user32.SetCursorPos(x, y)

    def _get_cursor_pos(self) -> Tuple[int, int]:
        pt = POINT()
        self._user32.GetCursorPos(ctypes.byref(pt))
        return pt.x, pt.y

    def _click(self, button: str):
        """Fires native mousedown and mouseup events instantly."""
        if button == "left":
            down, up = MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP
        elif button == "right":
            down, up = MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP
        else:
            raise ValueError(f"Unknown button: {button}")
            
        # Fire down then up
        self._user32.mouse_event(down, 0, 0, 0, 0)
        self._user32.mouse_event(up, 0, 0, 0, 0)
