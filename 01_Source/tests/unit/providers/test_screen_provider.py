"""
Tests for Screen Capture Provider.
"""

import pytest
import os
import asyncio
from unittest.mock import patch, MagicMock

from nova.providers.vision.screen_provider import ScreenCaptureProvider
from nova.providers.base import ProviderMetadata, ProviderType, ProviderRequest

@pytest.fixture
def provider():
    meta = ProviderMetadata(
        id="test.screen",
        name="Test",
        version="1.0",
        type=ProviderType.MOCK,
        description=""
    )
    prov = ScreenCaptureProvider(meta)
    return prov

@pytest.mark.asyncio
async def test_screen_provider_initializes(provider):
    await provider.initialize()
    assert os.path.exists(provider._output_dir)

@pytest.mark.asyncio
async def test_capture_active_monitor_mocked(provider):
    await provider.initialize()
    req = ProviderRequest(provider_id="test.screen", action="capture_active_monitor", payload={})
    
    with patch('mss.mss') as mock_mss, patch('PIL.Image.frombytes') as mock_img:
        mock_sct = MagicMock()
        mock_mss.return_value.__enter__.return_value = mock_sct
        
        # Mock monitors: index 0 is all, index 1 is primary
        mock_sct.monitors = [
            {"left": 0, "top": 0, "width": 3840, "height": 1080},
            {"left": 0, "top": 0, "width": 1920, "height": 1080}
        ]
        
        mock_sct_img = MagicMock()
        mock_sct_img.size = (1920, 1080)
        mock_sct_img.bgra = b'fakebytes'
        mock_sct.grab.return_value = mock_sct_img
        
        mock_image_instance = MagicMock()
        mock_img.return_value = mock_image_instance
        
        res = await provider.execute(req)
        
        assert "image_path" in res
        assert res["resolution"] == "1920x1080"
        mock_sct.grab.assert_called_once_with({"left": 0, "top": 0, "width": 1920, "height": 1080})
        mock_image_instance.save.assert_called_once()
