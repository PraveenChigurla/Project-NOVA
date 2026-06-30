"""
Observation Engine.
Observes the environment and continuously updates the World Model graph.
"""
import logging
from nova.intelligence.world.models import WorldGraph, Entity
from nova.intelligence.world.chronicle import EventChronicle

logger = logging.getLogger(__name__)

class ObservationEngine:
    """Updates the WorldGraph based on OS/Provider events."""
    
    def __init__(self, world_graph: WorldGraph, chronicle: EventChronicle):
        self.world = world_graph
        self.chronicle = chronicle
        
    def observe_initial_state(self):
        """
        Seeds the graph with the current state of the environment.
        In a real implementation, this would poll OS APIs or Providers.
        For Sprint 21, we manually inject entities to prove the graph logic.
        """
        logger.info("Observation Engine scanning initial state...")
        
        # Simulating observing Chrome running with a GitHub tab
        chrome_app = Entity(id="chrome_1", type="Application", attributes={"name": "Chrome"})
        chrome_win = Entity(id="chrome_win_1", type="Window", attributes={"focused": True})
        github_tab = Entity(id="tab_1", type="Tab", attributes={"url": "https://github.com", "title": "GitHub"})
        
        # Simulating VS Code running
        vscode_app = Entity(id="vscode_1", type="Application", attributes={"name": "VS Code"})
        nova_proj = Entity(id="proj_nova", type="Project", attributes={"path": "C:/Project NOVA"})
        
        # Add to graph
        for e in [chrome_app, chrome_win, github_tab, vscode_app, nova_proj]:
            self.world.add_entity(e)
            
        # Build relationships
        self.world.add_relationship("chrome_1", "chrome_win_1", "contains")
        self.world.add_relationship("chrome_win_1", "tab_1", "viewing")
        self.world.add_relationship("vscode_1", "proj_nova", "opened")
        
        self.chronicle.record("ObservationCompleted", {"entities_observed": len(self.world.entities)})
        logger.debug(f"World Graph seeded with {len(self.world.entities)} entities and {len(self.world.relationships)} relationships.")
