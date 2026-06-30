"""
Atomic Workspace Skills
"""
import os
import subprocess
import psutil

def launch_application(name: str, process_name: str, command: str) -> dict:
    """Check if app is running, launch if not."""
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and proc.info['name'].lower() == process_name.lower():
            return {"status": "skipped", "message": f"{name} is already running."}
            
    try:
        # Detached launch
        if os.name == 'nt':
            subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen(command, shell=True)
        return {"status": "launched", "message": f"{name} launched successfully."}
    except Exception as e:
        return {"status": "error", "message": f"Failed to launch {name}: {str(e)}"}

def open_repository(name: str, path: str, terminal: str = "windows_terminal", activate_env: bool = False) -> dict:
    """Open repository in preferred terminal."""
    if not os.path.exists(path):
        return {"status": "error", "message": f"Repository path not found: {path}"}
        
    term_cmd = "cmd.exe /c start cmd.exe"
    if terminal == "windows_terminal":
        term_cmd = f"wt.exe -d \"{path}\""
    elif terminal == "powershell":
        term_cmd = f"start powershell -NoExit -Command \"Set-Location -Path '{path}'\""
        
    try:
        subprocess.Popen(term_cmd, shell=True)
        env_msg = "Virtual environment activated." if activate_env else ""
        return {"status": "opened", "message": f"Repository {name} opened. {env_msg}"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to open repo {name}: {str(e)}"}

def git_status(path: str) -> dict:
    """Check git status."""
    if not os.path.exists(os.path.join(path, ".git")):
        return {"status": "skipped", "message": "Not a git repository."}
        
    result = subprocess.run(["git", "status", "--porcelain"], cwd=path, capture_output=True, text=True)
    if result.stdout.strip():
        return {"status": "dirty", "message": "Repository has uncommitted changes."}
    return {"status": "clean", "message": "Repository is clean."}

def git_pull(path: str) -> dict:
    """Pull, but halt on conflict."""
    if not os.path.exists(os.path.join(path, ".git")):
        return {"status": "skipped", "message": "Not a git repository."}
        
    result = subprocess.run(["git", "pull"], cwd=path, capture_output=True, text=True)
    out = result.stdout.lower() + result.stderr.lower()
    
    if "conflict" in out or "automatic merge failed" in out:
        return {
            "status": "conflict", 
            "message": "Git pull could not be completed. Merge conflicts detected.",
            "halt": True,
            "options": ["Open VS Code", "Open Merge Tool", "Show conflicting files", "Abort"]
        }
        
    if "up to date" in out or "up-to-date" in out:
         return {"status": "up_to_date", "message": "Already up to date."}
         
    if result.returncode != 0:
         return {"status": "error", "message": f"Git pull failed: {result.stderr.strip()}"}
         
    return {"status": "success", "message": "Successfully pulled latest changes."}

def open_website(name: str, url: str) -> dict:
    """Open a URL."""
    try:
        if os.name == 'nt':
            os.startfile(url)
        else:
            subprocess.Popen(["open" if sys.platform == "darwin" else "xdg-open", url])
        return {"status": "opened", "message": f"{name} opened."}
    except Exception as e:
        return {"status": "error", "message": f"Failed to open {name}: {str(e)}"}
