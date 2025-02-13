"""
Model configuration UI component
"""
import tkinter as tk
from tkinter import ttk
import json
from typing import Callable, Dict, Any
from src.utils.model_config import OllamaConfig
from src.utils.model_monitor import ModelMonitor

class ModelConfigUI:
    def __init__(self, parent: ttk.Frame):
        self.parent = parent
        self.config_manager = OllamaConfig()
        self.monitor = ModelMonitor()
        
        self.create_widgets()
        self.update_metrics()

    def create_widgets(self):
        """Create UI widgets"""
        # Configuration Frame
        config_frame = ttk.LabelFrame(self.parent, text="Model Configuration")
        config_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Context Window
        ttk.Label(config_frame, text="Context Window:").grid(row=0, column=0, padx=5, pady=5)
        self.context_window = tk.StringVar(value=str(self.config_manager.config["context_window"]))
        ttk.Entry(config_frame, textvariable=self.context_window).grid(row=0, column=1, padx=5, pady=5)

        # GPU Layers
        ttk.Label(config_frame, text="GPU Layers:").grid(row=1, column=0, padx=5, pady=5)
        self.gpu_layers = tk.StringVar(value=str(self.config_manager.config["gpu_layers"]))
        ttk.Entry(config_frame, textvariable=self.gpu_layers).grid(row=1, column=1, padx=5, pady=5)

        # Batch Size
        ttk.Label(config_frame, text="Batch Size:").grid(row=2, column=0, padx=5, pady=5)
        self.batch_size = tk.StringVar(value=str(self.config_manager.config["batch_size"]))
        ttk.Entry(config_frame, textvariable=self.batch_size).grid(row=2, column=1, padx=5, pady=5)

        # Threads
        ttk.Label(config_frame, text="Threads:").grid(row=3, column=0, padx=5, pady=5)
        self.num_thread = tk.StringVar(value=str(self.config_manager.config["num_thread"]))
        ttk.Entry(config_frame, textvariable=self.num_thread).grid(row=3, column=1, padx=5, pady=5)

        # Buttons
        button_frame = ttk.Frame(config_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Apply", command=self.apply_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Reset to Default", command=self.reset_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clean GPU", command=self.cleanup_gpu).pack(side=tk.LEFT, padx=5)

        # Metrics Frame
        metrics_frame = ttk.LabelFrame(self.parent, text="System Metrics")
        metrics_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.metrics_text = tk.Text(metrics_frame, height=10, width=50)
        self.metrics_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Update metrics every 5 seconds
        self.parent.after(5000, self.update_metrics)

    def apply_config(self):
        """Apply configuration changes"""
        new_config = {
            "context_window": int(self.context_window.get()),
            "gpu_layers": int(self.gpu_layers.get()),
            "batch_size": int(self.batch_size.get()),
            "num_thread": int(self.num_thread.get())
        }
        result = self.config_manager.update_config(new_config)
        if not result["success"]:
            tk.messagebox.showerror("Error", result["message"])

    def reset_config(self):
        """Reset to default configuration"""
        result = self.config_manager.reset_to_default()
        if result["success"]:
            self.context_window.set(str(self.config_manager.config["context_window"]))
            self.gpu_layers.set(str(self.config_manager.config["gpu_layers"]))
            self.batch_size.set(str(self.config_manager.config["batch_size"]))
            self.num_thread.set(str(self.config_manager.config["num_thread"]))
        else:
            tk.messagebox.showerror("Error", result["message"])

    def cleanup_gpu(self):
        """Clean up GPU memory"""
        result = self.monitor.cleanup_gpu_memory()
        if not result["success"]:
            tk.messagebox.showerror("Error", result["message"])

    def update_metrics(self):
        """Update system metrics display"""
        metrics = self.monitor.get_system_metrics()
        self.metrics_text.delete(1.0, tk.END)
        self.metrics_text.insert(tk.END, json.dumps(metrics, indent=2))
        
        # Schedule next update
        self.parent.after(5000, self.update_metrics)

    def save_metrics(self):
        """Save current metrics"""
        metrics = self.monitor.get_system_metrics()
        self.monitor.save_metrics(metrics)
