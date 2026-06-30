"""
NOVA Application Registry
Resolves generic semantic intents into concrete OS-specific applications.
"""
import os
import yaml
import platform

class AppRegistry:
    def __init__(self, config_dir: str):
        self.config_dir = config_dir
        self.apps_file = os.path.join(config_dir, "apps.yaml")
        self.prefs_file = os.path.join(config_dir, "preferences.yaml")
        self.catalog = self._load_yaml(self.apps_file) or {}
        self.prefs = self._load_yaml(self.prefs_file) or {}

    def _load_yaml(self, path: str):
        if not os.path.exists(path):
            return {}
        with open(path, 'r') as f:
            return yaml.safe_load(f)

    def _save_catalog(self):
        with open(self.apps_file, 'w') as f:
            yaml.dump(self.catalog, f, default_flow_style=False)

    def resolve_alias(self, alias: str) -> dict:
        """
        Attempts to resolve an alias (e.g. 'browser') to an application record.
        Checks preferences first, then aliases in the catalog.
        Returns the app record, or None if unknown.
        """
        alias_lower = alias.lower().strip()
        
        # 1. Check Preferences (e.g. "browser" -> preferences -> "chrome")
        if f"default_{alias_lower}" in self.prefs:
            app_id = self.prefs[f"default_{alias_lower}"]
            if app_id in self.catalog:
                return self._build_record(app_id, self.catalog[app_id])
                
        # 2. Check direct App ID
        if alias_lower in self.catalog:
            return self._build_record(alias_lower, self.catalog[alias_lower])
            
        # 3. Search aliases across the catalog
        for app_id, app_data in self.catalog.items():
            if alias_lower in [a.lower() for a in app_data.get("aliases", [])]:
                return self._build_record(app_id, app_data)
                
        return None

    def _build_record(self, app_id: str, app_data: dict) -> dict:
        os_name = platform.system().lower()
        if os_name == "windows":
            executables = app_data.get("executable", {}).get("windows", [])
        elif os_name == "darwin":
            executables = app_data.get("executable", {}).get("macos", [])
        else:
            executables = app_data.get("executable", {}).get("linux", [])
            
        return {
            "id": app_id,
            "executables": executables,
            "raw_data": app_data
        }

    def learn_alias(self, unknown_alias: str, app_id: str):
        """Learns a new alias for an existing application."""
        if app_id in self.catalog:
            if "aliases" not in self.catalog[app_id]:
                self.catalog[app_id]["aliases"] = []
            if unknown_alias not in self.catalog[app_id]["aliases"]:
                self.catalog[app_id]["aliases"].append(unknown_alias)
                self._save_catalog()
                return True
        return False
        
    def get_all_installed(self) -> list:
        # Stub for automated discovery
        return list(self.catalog.keys())
