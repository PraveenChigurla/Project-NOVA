"""
Intent Framework Models.
Defines the strict schemas for intents and entities.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class IntentEntity(BaseModel):
    """An extracted parameter from raw input."""
    name: str = Field(..., description="The name of the parameter (e.g., 'application')")
    value: Any = Field(..., description="The extracted value (e.g., 'notepad')")
    
    class Config:
        frozen = True

class IntentAlias(BaseModel):
    """Maps a trigger phrase or regex to a specific intent."""
    pattern: str = Field(..., description="The regex pattern to match")
    entities_map: Dict[int, str] = Field(default_factory=dict, description="Maps regex match groups to entity names")
    
    class Config:
        frozen = True

class Intent(BaseModel):
    """The definition of an intent that NOVA understands."""
    name: str = Field(..., description="The normalized intent name (e.g., 'desktop.process.launch')")
    description: str = Field(default="", description="Human readable description")
    required_entities: List[str] = Field(default_factory=list, description="List of entity names that MUST be present")
    aliases: List[IntentAlias] = Field(default_factory=list, description="List of trigger aliases for this intent")
    
    class Config:
        frozen = True

class IntentResult(BaseModel):
    """The normalized output sent to the Planner."""
    intent_name: str = Field(..., description="The matched normalized intent")
    entities: Dict[str, Any] = Field(default_factory=dict, description="The extracted parameters")
    confidence: float = Field(default=1.0, description="Confidence score between 0.0 and 1.0")
    original_input: str = Field(..., description="The raw input that generated this result")
    is_valid: bool = Field(default=True, description="Whether the required entities are satisfied")
    
    class Config:
        frozen = True
