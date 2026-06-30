"""
Constraint Engine.
Applies static or dynamic rules against the Context and State.
"""
import logging
from nova.intelligence.cognition.models import ContextSnapshot, ConstraintReport
from nova.intelligence.world.models import WorldGraph

logger = logging.getLogger(__name__)

class ConstraintEngine:
    """Evaluates environment constraints that the Planner must respect."""
    
    def evaluate(self, context: ContextSnapshot, world: WorldGraph) -> ConstraintReport:
        logger.debug("ConstraintEngine evaluating rules...")
        report = ConstraintReport()
        
        # Rule 1: Weekend Protection
        if context.day_of_week in ["Saturday", "Sunday"]:
            report.ask_user_confirmation = True
            report.skip_heavy_apps = True
            report.reasons.append("Weekend detected. Prompting before executing work tasks.")
            
        # Rule 2: Quiet Hours (e.g., after 10 PM)
        if context.hour >= 22 or context.hour <= 5:
            report.ask_user_confirmation = True
            report.reasons.append("Quiet hours active.")
            
        # Rule 3: Heavy Load (if IDE and Browser are both active, don't auto-launch more heavy stuff without asking)
        browser_apps = [e for e in world.get_entities_by_type("Application") if "chrome" in e.attributes.get("name", "").lower() or "msedge" in e.attributes.get("name", "").lower()]
        ide_apps = [e for e in world.get_entities_by_type("Application") if "code" in e.attributes.get("name", "").lower() or "vscode" in e.attributes.get("name", "").lower()]
        
        if browser_apps and ide_apps:
            report.reasons.append("System under moderate load. Planner should optimize for existing processes.")
            
        if report.reasons:
            for r in report.reasons:
                logger.info(f"Constraint Applied: {r}")
        else:
            logger.info("No active constraints. Execution is uninhibited.")
            
        return report
