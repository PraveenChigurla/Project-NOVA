"""
Tests for the LLM Contract Validator.
"""
import pytest
from nova.intelligence.llm.engines.validator import GoalContractValidator

def test_validator_valid_contract():
    validator = GoalContractValidator()
    
    raw = {
        "goal_id": "test_goal",
        "confidence": 0.9,
        "parameters": {},
        "requires_confirmation": False,
        "reasoning_summary": "Valid.",
        "safety_flags": []
    }
    
    contract = validator.validate(raw)
    assert contract.goal_id == "test_goal"
    assert contract.requires_confirmation == False

def test_validator_low_confidence_forces_confirmation():
    validator = GoalContractValidator()
    
    raw = {
        "goal_id": "test_goal",
        "confidence": 0.4,
        "parameters": {},
        "requires_confirmation": False, # LLM thinks it's fine
        "reasoning_summary": "Not sure.",
        "safety_flags": []
    }
    
    contract = validator.validate(raw)
    assert contract.requires_confirmation == True # Validator forced it

def test_validator_destructive_flag_forces_confirmation():
    validator = GoalContractValidator()
    
    raw = {
        "goal_id": "delete_files",
        "confidence": 0.99,
        "parameters": {},
        "requires_confirmation": False, # LLM thinks it's fine
        "reasoning_summary": "Delete everything.",
        "safety_flags": ["destructive"]
    }
    
    contract = validator.validate(raw)
    assert contract.requires_confirmation == True # Validator forced it
