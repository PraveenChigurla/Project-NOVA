"""
NOVA Goal Engine
Orchestrates high-level goals into atomic skills and produces Goal Reports.
"""
import time
import os
import yaml
from skills.workspace.operations import launch_application, open_repository, git_status, git_pull, open_website

class GoalEngine:
    def __init__(self, config_dir: str):
        self.config_dir = config_dir

    def run_workspace_prep(self, profile_name: str = "development") -> str:
        """Executes the Prepare Workspace Goal using the specified profile."""
        profile_path = os.path.join(self.config_dir, "profiles", f"{profile_name}.yaml")
        if not os.path.exists(profile_path):
            return f"[Error] Profile '{profile_name}' not found."
            
        with open(profile_path, 'r') as f:
            profile = yaml.safe_load(f)
            
        terminal = profile.get("preferred_terminal", "windows_terminal")
        
        report = []
        report.append(f"Goal: Prepare Workspace ({profile.get('name')})\n")
        report.append("Plan:")
        
        start_time = time.time()
        
        # 1. Applications
        for app in profile.get("applications", []):
            res = launch_application(app["name"], app["process_name"], app["launch_command"])
            if res["status"] == "skipped":
                report.append(f"✓ Launch {app['name']} (Skipped - Already running)")
            elif res["status"] == "launched":
                report.append(f"✓ Launch {app['name']} (Done)")
            else:
                report.append(f"✗ Launch {app['name']} (Failed: {res.get('message')})")
                
        # 2. Repositories & Git
        for repo in profile.get("repositories", []):
            res = open_repository(repo["name"], repo["path"], terminal, repo.get("activate_env", False))
            report.append(f"✓ Open Repository {repo['name']} (Done)")
            
            if repo.get("check_git", False):
                status_res = git_status(repo["path"])
                report.append(f"✓ Git Status (Done - {status_res['message']})")
                
                # Assume we want to pull
                pull_res = git_pull(repo["path"])
                if pull_res["status"] == "conflict":
                    report.append(f"✗ Pull Latest (Halted - Merge Conflicts)")
                    report.append("\n\033[91m[Action Required]\033[0m Git pull could not be completed.")
                    report.append("Merge conflicts detected. Would you like me to:")
                    for i, opt in enumerate(pull_res["options"]):
                        report.append(f"  {i+1}. {opt}")
                    report.append("\nExecution paused.")
                    break # Stop execution on conflict
                elif pull_res["status"] == "skipped":
                    report.append(f"✓ Pull Latest (Skipped - Not a repo)")
                elif pull_res["status"] == "up_to_date":
                    report.append(f"✓ Pull Latest (Skipped - Up to date)")
                else:
                    report.append(f"✓ Pull Latest (Done)")
                    
        # 3. Websites
        for site in profile.get("websites", []):
            res = open_website(site["name"], site["url"])
            report.append(f"✓ Open {site['name']} (Done)")
            
        duration = round(time.time() - start_time, 2)
        report.append(f"\nWorkspace ready. (Total Time: {duration}s)")
        
        return "\n".join(report)
