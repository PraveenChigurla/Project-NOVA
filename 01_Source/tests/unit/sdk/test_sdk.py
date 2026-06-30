"""
Tests for the SDK Validator.
"""
import os
import pytest
import shutil
import json
from nova.sdk.validator import ExtensionValidator

def test_validator_detects_missing_manifest(tmp_path):
    project_dir = tmp_path / "test_skill"
    project_dir.mkdir()
    
    # Missing manifest.json
    
    validator = ExtensionValidator()
    assert validator.validate(str(project_dir)) == False

def test_validator_detects_missing_src(tmp_path):
    project_dir = tmp_path / "test_skill"
    project_dir.mkdir()
    
    # Has manifest, missing src/
    manifest_path = project_dir / "manifest.json"
    manifest_path.write_text(json.dumps({
        "name": "test",
        "version": "1.0",
        "type": "skill",
        "permissions": [],
        "dependencies": []
    }))
    
    validator = ExtensionValidator()
    assert validator.validate(str(project_dir)) == False

def test_validator_passes_valid_structure(tmp_path):
    project_dir = tmp_path / "test_skill"
    project_dir.mkdir()
    
    manifest_path = project_dir / "manifest.json"
    manifest_path.write_text(json.dumps({
        "name": "test",
        "version": "1.0",
        "type": "skill",
        "permissions": [],
        "dependencies": []
    }))
    
    src_dir = project_dir / "src"
    src_dir.mkdir()
    
    main_py = src_dir / "main.py"
    main_py.write_text("class TestSkill: pass")
    
    validator = ExtensionValidator()
    assert validator.validate(str(project_dir)) == True
