"""
Default configuration settings handler
"""

import os
import json
from typing import Dict, Any, Optional
from pathlib import Path
import gradio as gr


class ConfigSettings:
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.settings = self.load_settings()

    def load_settings(self) -> Dict[str, Any]:
        """Load settings from JSON file"""
        config_file = Path(self.config_file)
        if config_file.exists():
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return self.get_default_settings()
        return self.get_default_settings()

    def save_settings(self):
        """Save settings to JSON file"""
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=4)

    def get_default_settings(self) -> Dict[str, Any]:
        """Get default configuration settings"""
        return {
            "agent_type": "custom",
            "max_steps": 100,
            "max_actions_per_step": 10,
            "use_vision": True,
            "tool_calling_method": "auto",
            "llm_provider": "openai",
            "llm_model_name": "gpt-4o",
            "llm_temperature": 1.0,
            "llm_base_url": "",
            "llm_api_key": "",
            "use_own_browser": os.getenv("CHROME_PERSISTENT_SESSION", "false").lower()
            == "true",
            "keep_browser_open": False,
            "headless": False,
            "disable_security": True,
            "enable_recording": True,
            "window_w": 1280,
            "window_h": 1100,
            "save_recording_path": "./tmp/record_videos",
            "save_trace_path": "./tmp/traces",
            "save_agent_history_path": "./tmp/agent_history",
            "task": "go to google.com and type 'OpenAI' click search and give me the first url",
        }

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value"""
        return self.settings.get(key, default)

    def set(self, key: str, value: Any):
        """Set a configuration value"""
        self.settings[key] = value
        self.save_settings()

    def update(self, settings: Dict[str, Any]):
        """Update multiple settings"""
        self.settings.update(settings)
        self.save_settings()


def save_current_config(*args):
    current_config = {
        "agent_type": args[0],
        "max_steps": args[1],
        "max_actions_per_step": args[2],
        "use_vision": args[3],
        "tool_calling_method": args[4],
        "llm_provider": args[5],
        "llm_model_name": args[6],
        "llm_temperature": args[7],
        "llm_base_url": args[8],
        "llm_api_key": args[9],
        "use_own_browser": args[10],
        "keep_browser_open": args[11],
        "headless": args[12],
        "disable_security": args[13],
        "enable_recording": args[14],
        "window_w": args[15],
        "window_h": args[16],
        "save_recording_path": args[17],
        "save_trace_path": args[18],
        "save_agent_history_path": args[19],
        "task": args[20],
    }
    config = ConfigSettings()
    config.update(current_config)
    return "Configuration saved successfully."


def update_ui_from_config(config_file):
    if config_file is not None:
        config = ConfigSettings(config_file.name)
        return (
            gr.update(value=config.get("agent_type", "custom")),
            gr.update(value=config.get("max_steps", 100)),
            gr.update(value=config.get("max_actions_per_step", 10)),
            gr.update(value=config.get("use_vision", True)),
            gr.update(value=config.get("tool_calling_method", "auto")),
            gr.update(value=config.get("llm_provider", "openai")),
            gr.update(value=config.get("llm_model_name", "gpt-4o")),
            gr.update(value=config.get("llm_temperature", 1.0)),
            gr.update(value=config.get("llm_base_url", "")),
            gr.update(value=config.get("llm_api_key", "")),
            gr.update(value=config.get("use_own_browser", False)),
            gr.update(value=config.get("keep_browser_open", False)),
            gr.update(value=config.get("headless", False)),
            gr.update(value=config.get("disable_security", True)),
            gr.update(value=config.get("enable_recording", True)),
            gr.update(value=config.get("window_w", 1280)),
            gr.update(value=config.get("window_h", 1100)),
            gr.update(value=config.get("save_recording_path", "./tmp/record_videos")),
            gr.update(value=config.get("save_trace_path", "./tmp/traces")),
            gr.update(
                value=config.get("save_agent_history_path", "./tmp/agent_history")
            ),
            gr.update(value=config.get("task", "")),
            "Configuration loaded successfully.",
        )
    return (
        gr.update(),
        gr.update(),
        gr.update(),
        gr.update(),
        gr.update(),
        gr.update(),
        gr.update(),
        gr.update(),
        gr.update(),
        gr.update(),
        gr.update(),
        gr.update(),
        gr.update(),
        gr.update(),
        gr.update(),
        gr.update(),
        gr.update(),
        gr.update(),
        gr.update(),
        gr.update(),
        gr.update(),
        "No file selected.",
    )
