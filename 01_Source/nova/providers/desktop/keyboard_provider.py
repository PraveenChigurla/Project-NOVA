"""
Keyboard Provider.
Exposes low-level Win32 keyboard primitives using ctypes SendInput for Unicode safety.
"""
import ctypes
import logging
from typing import Dict, Any, Optional, List

from nova.providers.base import Provider, ProviderRequest, ProviderContext, ProviderMetadata, ProviderType

logger = logging.getLogger(__name__)

# --- Win32 API Constants & Structures ---
INPUT_KEYBOARD = 1
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004

class KEYBDINPUT(ctypes.Structure):
    _fields_ = (
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
    )

class INPUT_union(ctypes.Union):
    _fields_ = (
        ("ki", KEYBDINPUT),
        ("mi", ctypes.c_ulong * 7), # Padding for Mouse
        ("hi", ctypes.c_ulong * 4)  # Padding for Hardware
    )

class INPUT(ctypes.Structure):
    _fields_ = (
        ("type", ctypes.c_ulong),
        ("union", INPUT_union)
    )

class KeyboardProvider(Provider):
    """
    Low-level keyboard controller. 
    Does not implement typing speed; that is the Capability's job.
    """
    
    def __init__(self, metadata: ProviderMetadata):
        super().__init__(metadata)
        self._user32 = ctypes.windll.user32
            
    async def initialize(self) -> None:
        logger.info(f"[{self.metadata.id}] Initializing Keyboard Provider...")
        
    async def start(self) -> None:
        logger.info(f"[{self.metadata.id}] Keyboard Provider Online.")
        
    async def execute(self, request: ProviderRequest, context: Optional[ProviderContext] = None) -> Dict[str, Any]:
        logger.debug(f"[{self.metadata.id}] Native Action: {request.action}")
        
        if request.action == "type_text":
            text = request.payload.get("text", "")
            self._type_unicode(text)
            return {"status": "typed", "length": len(text)}
            
        elif request.action == "press_key":
            # Implementation for hotkeys (e.g. VK_RETURN) would go here
            # For brevity in this sprint, we focus on unicode strings
            return {"status": "ignored_in_demo"}
            
        raise ValueError(f"KeyboardProvider does not support action: '{request.action}'")

    async def stop(self) -> None:
        pass
        
    async def shutdown(self) -> None:
        pass

    # =========================================================================
    # NATIVE CTYPES IMPLEMENTATIONS (SendInput)
    # =========================================================================

    def _type_unicode(self, text: str):
        """Types a string using native Unicode injection, bypassing layout issues."""
        inputs = []
        for char in text:
            # Down press
            inp_down = INPUT()
            inp_down.type = INPUT_KEYBOARD
            inp_down.union.ki = KEYBDINPUT(0, ord(char), KEYEVENTF_UNICODE, 0, None)
            inputs.append(inp_down)
            
            # Up press
            inp_up = INPUT()
            inp_up.type = INPUT_KEYBOARD
            inp_up.union.ki = KEYBDINPUT(0, ord(char), KEYEVENTF_UNICODE | KEYEVENTF_KEYUP, 0, None)
            inputs.append(inp_up)
            
        if inputs:
            # SendInput requires an array of INPUT structures
            arr = (INPUT * len(inputs))(*inputs)
            self._user32.SendInput(len(inputs), ctypes.byref(arr), ctypes.sizeof(INPUT))
