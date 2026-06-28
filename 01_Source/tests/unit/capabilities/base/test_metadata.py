import pytest
from pydantic import ValidationError
from nova.capabilities.base.metadata import CapabilityMetadata

def test_metadata_valid_creation():
    """Test valid instantiation of CapabilityMetadata."""
    meta = CapabilityMetadata(
        id="com.nova.test",
        name="Test Capability",
        version="1.0.0",
        description="A test capability",
        permissions_required=["os.read"],
        dependencies=["com.nova.other"]
    )
    
    assert meta.id == "com.nova.test"
    assert meta.name == "Test Capability"
    assert "os.read" in meta.permissions_required
    assert meta.author is None

def test_metadata_immutability():
    """Test that CapabilityMetadata is strictly immutable."""
    meta = CapabilityMetadata(
        id="com.nova.test",
        name="Test Capability",
        version="1.0.0",
        description="A test capability"
    )
    
    with pytest.raises(ValidationError):
        meta.id = "new.id"

def test_metadata_missing_required_fields():
    """Test that missing required fields raises a ValidationError."""
    with pytest.raises(ValidationError):
        CapabilityMetadata(id="com.nova.test")  # Missing name, version, description

def test_metadata_json_serialization():
    """Test JSON dump and load functionality."""
    meta = CapabilityMetadata(
        id="com.nova.test",
        name="Test",
        version="1.0",
        description="Desc"
    )
    json_data = meta.model_dump_json()
    assert "com.nova.test" in json_data
    
    meta2 = CapabilityMetadata.model_validate_json(json_data)
    assert meta2.id == meta.id
