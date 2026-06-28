"""
Tests for Capability Registry Validator.
"""

import pytest
from nova.capabilities.registry.validator import DependencyValidator, CircularDependencyError, MissingDependencyError

def test_valid_dependency_graph():
    validator = DependencyValidator()
    # A -> B -> C
    validator.add_capability("A", ["B"])
    validator.add_capability("B", ["C"])
    validator.add_capability("C", [])
    
    # Should not raise
    validator.validate_graph()

def test_missing_dependency():
    validator = DependencyValidator()
    validator.add_capability("A", ["B"])
    # B is missing
    
    with pytest.raises(MissingDependencyError):
        validator.validate_graph()

def test_circular_dependency():
    validator = DependencyValidator()
    # A -> B -> C -> A
    validator.add_capability("A", ["B"])
    validator.add_capability("B", ["C"])
    validator.add_capability("C", ["A"])
    
    with pytest.raises(CircularDependencyError):
        validator.validate_graph()
