"""
Workflow Compiler.
Converts declarative YAML workflows into executable Plans.
"""
import os
import yaml
import logging
from typing import Dict, Any, List

from nova.skills.models import SkillManifest, SkillContext
from nova.intelligence.planning.models import ExecutionPlan, PlanStep, ExecutionStrategy

logger = logging.getLogger(__name__)

class WorkflowCompiler:
    """Compiles a Skill's declarative workflow into a NOVA ExecutionPlan."""
    
    def compile(self, manifest: SkillManifest, context: SkillContext, vault=None) -> ExecutionPlan:
        """Reads the entrypoint workflow and resolves variables."""
        workflow_path = os.path.join(manifest.package_path, manifest.entrypoint)
        
        if not os.path.exists(workflow_path):
            raise FileNotFoundError(f"Workflow entrypoint '{manifest.entrypoint}' not found in {manifest.package_path}")
            
        try:
            with open(workflow_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except Exception as e:
            raise ValueError(f"Failed to parse workflow YAML: {e}")
            
        raw_steps = data.get("steps", [])
        if not raw_steps:
            logger.warning(f"Workflow '{manifest.id}' has no steps defined.")
            
        plan_steps = []
        for i, raw_step in enumerate(raw_steps):
            # 1. Resolve template variables (e.g. ${username} or ${vault:github.main.password})
            resolved_parameters = self._resolve_parameters(raw_step.get("parameters", {}), context.parameters, manifest.id, vault)
            
            # 2. Build PlanStep
            step = PlanStep(
                step_id=f"{manifest.id}_step_{i}",
                capability_id=raw_step.get("capability", "unknown"),
                action=raw_step.get("action", "unknown"),
                parameters=resolved_parameters,
                dependencies=[] # For now, simple sequential execution
            )
            plan_steps.append(step)
            
        # 3. Assemble Plan
        plan = ExecutionPlan(
            intent=f"Execute Skill: {manifest.id}",
            strategy=ExecutionStrategy.SEQUENTIAL,
            steps=plan_steps
        )
        
        logger.info(f"Compiled Skill '{manifest.id}' into ExecutionPlan with {len(plan_steps)} steps.")
        return plan
        
    def _resolve_parameters(self, raw_params: Dict[str, Any], context_params: Dict[str, Any], skill_id: str, vault=None) -> Dict[str, Any]:
        """Replaces string literals like '${name}' or '${vault:id.key}' with actual values."""
        resolved = {}
        for k, v in raw_params.items():
            if isinstance(v, str) and v.startswith("${") and v.endswith("}"):
                var_name = v[2:-1] # Extract 'name' from '${name}'
                
                # Check for Vault injection
                if var_name.startswith("vault:"):
                    if not vault:
                        raise RuntimeError(f"Skill '{skill_id}' requested a vault secret, but no Vault is attached.")
                    
                    vault_path = var_name[6:] # e.g. "github.main.username"
                    parts = vault_path.rsplit(".", 1)
                    if len(parts) != 2:
                        raise ValueError(f"Invalid vault path syntax: {vault_path}. Expected 'identity_id.credential_key'")
                        
                    identity_id, cred_key = parts[0], parts[1]
                    secret_val = vault.get_credential(identity_id, cred_key, accessor_id=f"skill:{skill_id}")
                    
                    if secret_val is None:
                        raise RuntimeError(f"Skill '{skill_id}' failed to retrieve secret: {vault_path}")
                        
                    resolved[k] = secret_val
                else:
                    # Inject value from context, or fallback to the raw template string if missing
                    resolved[k] = context_params.get(var_name, v)
            else:
                resolved[k] = v
        return resolved
