"""
Model configuration manager for Ollama
"""
import json
import requests
from typing import Dict, Any, Optional
from pathlib import Path

class OllamaConfig:
    def __init__(self, config_file: str = "config/ollama_config.json"):
        self.config_file = Path(config_file)
        self.default_config = {
            "model": "deepseek-r1:70b",
            "gpu_layers": 68,
            "context_window": 8192,
            "num_gpu": 1,
            "num_thread": 16,
            "batch_size": 8,
            "tensor_split": [1],
            "cuda_memory_fraction": 0.9,
            "rope_scaling": {
                "type": "dynamic",
                "factor": 2.0
            },
            "f16_kv": True,
            "use_mmap": True,
            "numa": False,
            "low_vram": False
        }
        self.load_config()

    def load_config(self):
        """Load configuration from file"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = self.default_config.copy()
            self.save_config()

    def save_config(self):
        """Save configuration to file"""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)

    def update_config(self, new_config: Dict[str, Any]):
        """Update configuration"""
        self.config.update(new_config)
        self.save_config()
        return self.apply_config()

    def reset_to_default(self):
        """Reset configuration to default"""
        self.config = self.default_config.copy()
        self.save_config()
        return self.apply_config()

    def apply_config(self) -> Dict[str, Any]:
        """Apply configuration to running Ollama instance"""
        try:
            # Update model configuration via Ollama API
            response = requests.post(
                'http://localhost:11434/api/generate',
                json={
                    "model": self.config["model"],
                    "context_window": self.config["context_window"],
                    "num_gpu": self.config["num_gpu"],
                    "num_thread": self.config["num_thread"],
                    "batch_size": self.config["batch_size"],
                    "parameters": {
                        "gpu_layers": self.config["gpu_layers"],
                        "rope_scaling": self.config["rope_scaling"],
                        "f16_kv": self.config["f16_kv"],
                        "use_mmap": self.config["use_mmap"],
                        "numa": self.config["numa"],
                        "low_vram": self.config["low_vram"]
                    }
                },
                timeout=5
            )
            response.raise_for_status()
            return {"success": True, "message": "Configuration applied successfully"}
        except requests.exceptions.RequestException as e:
            return {"success": False, "message": f"Failed to apply configuration: {str(e)}"}

    def get_config(self) -> Dict[str, Any]:
        """Get current configuration"""
        return self.config

    def get_model_info(self) -> Optional[Dict[str, Any]]:
        """Get information about the running model"""
        try:
            response = requests.get('http://localhost:11434/api/show', timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return None
