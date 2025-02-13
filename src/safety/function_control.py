"""
Function Control System for Web UI
"""

import os
import json
from typing import Dict, List, Optional
from pathlib import Path


class FunctionControl:
    def __init__(self):
        self.config_path = Path("config/function_control.json")
        self.blacklist_path = Path("config/function_blacklist.json")
        self.disabled_functions: Dict[str, Dict] = {}
        self.blacklisted_patterns: List[str] = []
        self.load_config()

    def load_config(self):
        """Load function control configuration"""
        # Create config directory if it doesn't exist
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        # Load disabled functions
        if self.config_path.exists():
            with open(self.config_path, "r") as f:
                self.disabled_functions = json.load(f)
        else:
            self.save_config()

        # Load blacklist
        if self.blacklist_path.exists():
            with open(self.blacklist_path, "r") as f:
                self.blacklisted_patterns = json.load(f)
        else:
            # Default blacklist patterns
            self.blacklisted_patterns = [
                "delete_*",
                "remove_*",
                "format_*",
                "wipe_*",
                "system_*",
                "registry_*",
                "network_*",
                "firewall_*",
                "install_*",
                "uninstall_*",
                "download_*",
                "execute_*",
                "run_*",
                "modify_*",
                "change_*",
            ]
            self.save_blacklist()

    def save_config(self):
        """Save function control configuration"""
        with open(self.config_path, "w") as f:
            json.dump(self.disabled_functions, f, indent=4)

    def save_blacklist(self):
        """Save blacklist patterns"""
        with open(self.blacklist_path, "w") as f:
            json.dump(self.blacklisted_patterns, f, indent=4)

    def disable_function(self, name: str, reason: str = ""):
        """
        Disable a function

        Args:
            name: Name of the function to disable
            reason: Reason for disabling
        """
        self.disabled_functions[name] = {
            "disabled": True,
            "reason": reason,
            "timestamp": str(datetime.now()),
        }
        self.save_config()

    def enable_function(self, name: str):
        """
        Enable a function

        Args:
            name: Name of the function to enable
        """
        if name in self.disabled_functions:
            del self.disabled_functions[name]
            self.save_config()

    def is_function_allowed(self, name: str) -> bool:
        """
        Check if a function is allowed

        Args:
            name: Name of the function to check

        Returns:
            bool: True if function is allowed, False otherwise
        """
        # Check if explicitly disabled
        if name in self.disabled_functions:
            return False

        # Check against blacklist patterns
        import fnmatch

        return not any(
            fnmatch.fnmatch(name, pattern) for pattern in self.blacklisted_patterns
        )

    def get_function_status(self, name: str) -> Dict:
        """
        Get status of a function

        Args:
            name: Name of the function to check

        Returns:
            dict: Function status information
        """
        if name in self.disabled_functions:
            return self.disabled_functions[name]
        return {"disabled": False, "reason": "", "timestamp": ""}

    def add_blacklist_pattern(self, pattern: str):
        """
        Add a pattern to the blacklist

        Args:
            pattern: Pattern to add
        """
        if pattern not in self.blacklisted_patterns:
            self.blacklisted_patterns.append(pattern)
            self.save_blacklist()

    def remove_blacklist_pattern(self, pattern: str):
        """
        Remove a pattern from the blacklist

        Args:
            pattern: Pattern to remove
        """
        if pattern in self.blacklisted_patterns:
            self.blacklisted_patterns.remove(pattern)
            self.save_blacklist()

    def get_all_disabled_functions(self) -> Dict[str, Dict]:
        """Get all disabled functions"""
        return self.disabled_functions

    def get_blacklist(self) -> List[str]:
        """Get all blacklist patterns"""
        return self.blacklisted_patterns


# Global instance
function_control = FunctionControl()
