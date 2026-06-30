"""
Tests for the Skill Runtime Framework.
"""
import pytest
from nova.skills.models import SkillManifest, SkillContext
from nova.skills.compiler import WorkflowCompiler

def test_workflow_compiler_resolves_parameters():
    compiler = WorkflowCompiler()
    
    raw_params = {
        "text": "Hello ${name}!",
        "age": "${user_age}"
    }
    
    context_params = {
        "name": "Praveen",
        "user_age": 30
    }
    
    resolved = compiler._resolve_parameters(raw_params, context_params)
    
    assert resolved["text"] == "Hello Praveen!"
    assert resolved["age"] == 30
    
def test_workflow_compiler_missing_parameter_fallback():
    compiler = WorkflowCompiler()
    
    raw_params = {
        "text": "Hello ${missing_var}!"
    }
    
    context_params = {}
    
    resolved = compiler._resolve_parameters(raw_params, context_params)
    
    # Should fallback to the literal string if not provided in context
    assert resolved["text"] == "Hello ${missing_var}!"
