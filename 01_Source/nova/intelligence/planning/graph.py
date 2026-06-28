"""
Task Graph.
Validates dependencies and computes parallel execution layers for PlanSteps.
"""

from typing import List, Dict, Set
from nova.intelligence.planning.models import PlanStep

class TaskGraphError(Exception):
    pass

class CircularDependencyError(TaskGraphError):
    pass

class MissingDependencyError(TaskGraphError):
    pass

class TaskGraph:
    """
    Represents the ExecutionPlan as a Directed Acyclic Graph (DAG).
    """
    def __init__(self, steps: List[PlanStep]):
        self.steps = steps
        self._step_map = {step.step_id: step for step in steps}
        
    def validate(self) -> None:
        """
        Validates the graph for missing dependencies and cycles.
        Raises TaskGraphError if the graph is invalid.
        """
        # Check for missing dependencies
        for step in self.steps:
            for dep_id in step.dependencies:
                if dep_id not in self._step_map:
                    raise MissingDependencyError(f"Step '{step.step_id}' depends on missing step '{dep_id}'")
                    
        # Check for cycles using DFS (0=unvisited, 1=visiting, 2=visited)
        state: Dict[str, int] = {step.step_id: 0 for step in self.steps}
        
        def dfs(node_id: str) -> None:
            if state[node_id] == 1:
                raise CircularDependencyError(f"Circular dependency detected involving step '{node_id}'")
            if state[node_id] == 2:
                return
                
            state[node_id] = 1
            step = self._step_map[node_id]
            for dep_id in step.dependencies:
                dfs(dep_id)
            state[node_id] = 2

        for step in self.steps:
            if state[step.step_id] == 0:
                dfs(step.step_id)

    def get_execution_layers(self) -> List[List[PlanStep]]:
        """
        Computes the layers of execution for parallel processing.
        Returns a list of layers, where each layer is a list of independent PlanSteps.
        """
        self.validate()
        
        in_degree: Dict[str, int] = {step.step_id: 0 for step in self.steps}
        adj_list: Dict[str, List[str]] = {step.step_id: [] for step in self.steps}
        
        for step in self.steps:
            for dep_id in step.dependencies:
                adj_list[dep_id].append(step.step_id)
                in_degree[step.step_id] += 1
                
        layers = []
        # Find all nodes with 0 in-degree
        current_layer = [sid for sid in in_degree if in_degree[sid] == 0]
        
        while current_layer:
            # Add current layer to output
            layers.append([self._step_map[sid] for sid in current_layer])
            
            next_layer = []
            for sid in current_layer:
                for neighbor in adj_list[sid]:
                    in_degree[neighbor] -= 1
                    if in_degree[neighbor] == 0:
                        next_layer.append(neighbor)
                        
            current_layer = next_layer
            
        return layers
