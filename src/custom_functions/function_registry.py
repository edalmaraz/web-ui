"""
Function registry for managing custom functions
"""

import importlib
import inspect
import logging
import os
from typing import Dict, Any, Callable
from browser_use.agent.views import ActionResult
from browser_use.browser.context import BrowserContext

logger = logging.getLogger(__name__)


class FunctionRegistry:
    def __init__(self):
        self.functions: Dict[str, Callable] = {}
        self.browser_required: Dict[str, bool] = {}

    def register(self, name: str, requires_browser: bool = False):
        """Decorator to register a function"""

        def decorator(func):
            self.functions[name] = func
            self.browser_required[name] = requires_browser
            return func

        return decorator

    def load_functions_from_directory(self, directory: str):
        """Load all functions from .py files in the specified directory"""
        for filename in os.listdir(directory):
            if filename.endswith(".py") and not filename.startswith("_"):
                module_name = filename[:-3]  # Remove .py extension
                try:
                    # Import the module
                    module = importlib.import_module(
                        f"src.custom_functions.{module_name}"
                    )

                    # Look for functions decorated with @registry.action
                    for name, obj in inspect.getmembers(module):
                        if hasattr(obj, "_is_custom_action"):
                            action_name = getattr(obj, "_action_name")
                            requires_browser = getattr(obj, "_requires_browser", False)
                            self.functions[action_name] = obj
                            self.browser_required[action_name] = requires_browser

                    logger.info(f"Loaded functions from {module_name}")
                except Exception as e:
                    logger.error(f"Error loading module {module_name}: {str(e)}")

    def get_function(self, name: str) -> Callable:
        """Get a registered function by name"""
        return self.functions.get(name)

    def requires_browser(self, name: str) -> bool:
        """Check if a function requires browser access"""
        return self.browser_required.get(name, False)

    def list_functions(self) -> Dict[str, Dict[str, Any]]:
        """List all registered functions and their metadata"""
        result = {}
        for name, func in self.functions.items():
            # Get function signature
            sig = inspect.signature(func)

            # Get parameter info
            params = {}
            for param_name, param in sig.parameters.items():
                if param_name != "browser":  # Skip browser parameter
                    params[param_name] = str(param.annotation.__name__)

            result[name] = {
                "requires_browser": self.browser_required[name],
                "parameters": params,
                "docstring": func.__doc__ or "No description available",
            }
        return result


# Create global registry instance
registry = FunctionRegistry()
