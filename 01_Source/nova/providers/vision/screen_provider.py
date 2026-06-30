"""
Screen Capture Provider.
Acquires high-performance images from the operating system.
"""

from typing import Dict, Any, Optional
import logging
import os
import mss
from PIL import Image

from nova.providers.base import (
    Provider,
    ProviderRequest,
    ProviderContext,
    ProviderError
)

logger = logging.getLogger(__name__)

class ScreenCaptureProvider(Provider):
    """
    Acquires screen captures natively.
    No OCR or ML inference is performed here.
    """
    
    async def initialize(self) -> None:
        logger.info(f"[{self.metadata.id}] Initializing Screen Capture Provider...")
        self._output_dir = os.path.join(os.getcwd(), "01_Source", ".temp_captures")
        os.makedirs(self._output_dir, exist_ok=True)
        
    async def start(self) -> None:
        logger.info(f"[{self.metadata.id}] Screen Capture Provider Online.")
        
    async def execute(self, request: ProviderRequest, context: Optional[ProviderContext] = None) -> Dict[str, Any]:
        """Route the requested action to the correct subsystem."""
        logger.info(f"[{self.metadata.id}] Executing native action: {request.action}")
        
        output_path = os.path.join(self._output_dir, f"capture_{request.provider_id}.png")
        
        if request.action == "capture_full_desktop":
            return await self._capture_screen(output_path, monitor_idx=-1)
            
        elif request.action == "capture_active_monitor":
            return await self._capture_screen(output_path, monitor_idx=1) # 1 is usually primary/active in mss, can be dynamic
            
        elif request.action == "capture_monitor":
            monitor_idx = request.payload.get("monitor_index", 1)
            return await self._capture_screen(output_path, monitor_idx=monitor_idx)
            
        elif request.action == "capture_region":
            bounds = request.payload.get("bounds", {})
            return await self._capture_region(output_path, bounds)
            
        raise ValueError(f"ScreenCaptureProvider does not support action: '{request.action}'")

    async def stop(self) -> None:
        logger.info(f"[{self.metadata.id}] Screen Capture Provider Offline.")
        
    async def shutdown(self) -> None:
        logger.info(f"[{self.metadata.id}] Shutting down.")

    # =========================================================================
    # IMPLEMENTATIONS
    # =========================================================================

    async def _capture_screen(self, output_path: str, monitor_idx: int) -> Dict[str, Any]:
        """Captures a specific monitor or the entire virtual desktop."""
        try:
            with mss.mss() as sct:
                # monitor_idx -1 means all monitors in mss. 1 is first monitor.
                monitors = sct.monitors
                if monitor_idx >= len(monitors):
                    raise ValueError(f"Monitor index {monitor_idx} out of range. (Available: {len(monitors)-1})")
                
                # In mss, index 0 is a special 'all monitors stitched together'
                # index 1 is primary monitor.
                target_idx = 0 if monitor_idx == -1 else monitor_idx
                
                monitor = monitors[target_idx]
                sct_img = sct.grab(monitor)
                
                # Save via Pillow for compression/formatting if needed, or directly via mss
                img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
                img.save(output_path, "PNG")
                
                return {
                    "image_path": output_path,
                    "bounds": monitor,
                    "resolution": f"{monitor['width']}x{monitor['height']}"
                }
        except Exception as e:
            raise RuntimeError(f"Failed to capture screen: {e}")

    async def _capture_region(self, output_path: str, bounds: Dict[str, int]) -> Dict[str, Any]:
        """Captures a specific arbitrary bounding box."""
        try:
            required = ["left", "top", "width", "height"]
            if not all(k in bounds for k in required):
                raise ValueError(f"Bounds must contain {required}")
                
            monitor = {
                "left": bounds["left"],
                "top": bounds["top"],
                "width": bounds["width"],
                "height": bounds["height"]
            }
            
            with mss.mss() as sct:
                sct_img = sct.grab(monitor)
                img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
                img.save(output_path, "PNG")
                
                return {
                    "image_path": output_path,
                    "bounds": monitor,
                    "resolution": f"{monitor['width']}x{monitor['height']}"
                }
        except Exception as e:
            raise RuntimeError(f"Failed to capture region: {e}")
