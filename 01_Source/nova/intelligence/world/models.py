"""
World Model Definitions.
Provides a graph-based representation of NOVA's perceived reality.
"""
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class Entity(BaseModel):
    """A node in the World Model Graph."""
    id: str = Field(..., description="Unique identifier for the entity (e.g., 'chrome_main', 'vscode_nova')")
    type: str = Field(..., description="Entity type (e.g., 'Application', 'Window', 'Tab', 'Project')")
    attributes: Dict[str, Any] = Field(default_factory=dict)
    
class Relationship(BaseModel):
    """An edge in the World Model Graph."""
    source_id: str
    target_id: str
    type: str = Field(..., description="Relationship type (e.g., 'contains', 'viewing', 'running')")

class WorldGraph(BaseModel):
    """A lightweight, in-memory directed graph of the environment."""
    entities: Dict[str, Entity] = Field(default_factory=dict)
    relationships: List[Relationship] = Field(default_factory=list)
    
    def add_entity(self, entity: Entity):
        self.entities[entity.id] = entity
        
    def add_relationship(self, source_id: str, target_id: str, rel_type: str):
        if source_id in self.entities and target_id in self.entities:
            self.relationships.append(Relationship(source_id=source_id, target_id=target_id, type=rel_type))
            
    def get_related(self, entity_id: str, rel_type: Optional[str] = None) -> List[Entity]:
        """Returns all targets connected to the given source, optionally filtered by relationship type."""
        related = []
        for r in self.relationships:
            if r.source_id == entity_id:
                if rel_type is None or r.type == rel_type:
                    if r.target_id in self.entities:
                        related.append(self.entities[r.target_id])
        return related
        
    def get_entities_by_type(self, entity_type: str) -> List[Entity]:
        return [e for e in self.entities.values() if e.type == entity_type]
