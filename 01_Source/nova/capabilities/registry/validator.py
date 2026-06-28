"""
Capability Dependency Validator.
Performs topological sorting and cycle detection on capability manifests.
"""

from typing import Dict, List, Set

class DependencyError(Exception):
    """Base exception for dependency validation failures."""
    pass

class CircularDependencyError(DependencyError):
    """Raised when a dependency cycle is detected."""
    pass

class MissingDependencyError(DependencyError):
    """Raised when a required capability is not available."""
    pass

class DependencyValidator:
    """
    Validates capability dependency graphs.
    """
    def __init__(self):
        # adjacency list representation: {capability_id: [dependency_ids]}
        self._graph: Dict[str, List[str]] = {}

    def add_capability(self, capability_id: str, dependencies: List[str]) -> None:
        """Register a capability and its dependencies to the graph."""
        self._graph[capability_id] = dependencies

    def validate_graph(self) -> None:
        """
        Validate the entire graph.
        Checks for missing capabilities and circular dependencies.
        Raises DependencyError if the graph is invalid.
        """
        self._check_missing()
        self._check_cycles()

    def _check_missing(self) -> None:
        """Ensure all declared dependencies exist in the graph."""
        available_nodes = set(self._graph.keys())
        for node, deps in self._graph.items():
            for dep in deps:
                if dep not in available_nodes:
                    raise MissingDependencyError(
                        f"Capability '{node}' depends on missing capability '{dep}'"
                    )

    def _check_cycles(self) -> None:
        """
        Detect cycles using Depth First Search (DFS).
        Colors: 0=Unvisited, 1=Visiting, 2=Visited.
        """
        visited_state: Dict[str, int] = {node: 0 for node in self._graph}

        def dfs(node: str, path: List[str]) -> None:
            visited_state[node] = 1
            path.append(node)
            
            for neighbor in self._graph.get(node, []):
                if visited_state[neighbor] == 1:
                    cycle = " -> ".join(path + [neighbor])
                    raise CircularDependencyError(f"Circular dependency detected: {cycle}")
                elif visited_state[neighbor] == 0:
                    dfs(neighbor, path)
            
            path.pop()
            visited_state[node] = 2

        for node in self._graph:
            if visited_state[node] == 0:
                dfs(node, [])
