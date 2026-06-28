"""
Tests for Windows Desktop Provider.
"""

import pytest
import os
from unittest.mock import patch, MagicMock

from nova.providers.desktop.provider import WindowsDesktopProvider
from nova.providers.base import ProviderMetadata, ProviderType, ProviderRequest

@pytest.fixture
def provider():
    meta = ProviderMetadata(
        id="test.desktop",
        name="Test",
        version="1.0",
        type=ProviderType.DESKTOP,
        description=""
    )
    return WindowsDesktopProvider(meta)

@pytest.mark.asyncio
async def test_launch_process(provider):
    if os.name != 'nt':
        pytest.skip("Windows only")
        
    req = ProviderRequest(provider_id="test.desktop", action="launch_process", payload={"executable": "cmd.exe"})
    
    with patch('subprocess.Popen') as mock_popen:
        mock_process = MagicMock()
        mock_process.pid = 1234
        mock_popen.return_value = mock_process
        
        res = await provider._launch_process(req.payload.get("executable"))
        
        assert res["status"] == "launched"
        assert res["pid"] == 1234
        mock_popen.assert_called_once_with("cmd.exe", shell=True)

@pytest.mark.asyncio
async def test_terminate_process(provider):
    if os.name != 'nt':
        pytest.skip("Windows only")
        
    with patch('subprocess.run') as mock_run:
        await provider._terminate_process("cmd.exe")
        mock_run.assert_called_once_with(["taskkill", "/F", "/IM", "cmd.exe"], check=True, capture_output=True)
