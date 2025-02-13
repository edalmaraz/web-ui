"""
Model monitoring utilities
"""
import psutil
import GPUtil
from typing import Dict, Any
import subprocess
import json
from pathlib import Path

class ModelMonitor:
    def __init__(self):
        self.gpu_indices = GPUtil.getAvailable(order='memory', limit=1, maxLoad=0.5, maxMemory=0.5)

    def get_system_metrics(self) -> Dict[str, Any]:
        """Get current system metrics"""
        metrics = {
            "cpu": {
                "usage_percent": psutil.cpu_percent(interval=1),
                "memory_percent": psutil.virtual_memory().percent,
                "threads": psutil.cpu_count(),
            },
            "gpu": self._get_gpu_metrics(),
            "memory": {
                "total": psutil.virtual_memory().total / (1024 ** 3),  # GB
                "available": psutil.virtual_memory().available / (1024 ** 3),  # GB
                "used": psutil.virtual_memory().used / (1024 ** 3),  # GB
            }
        }
        return metrics

    def _get_gpu_metrics(self) -> Dict[str, Any]:
        """Get GPU metrics using nvidia-smi"""
        try:
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=temperature.gpu,utilization.gpu,memory.used,memory.total', '--format=csv,noheader,nounits'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                temp, util, mem_used, mem_total = map(float, result.stdout.strip().split(','))
                return {
                    "temperature": temp,
                    "utilization": util,
                    "memory": {
                        "used": mem_used,
                        "total": mem_total,
                        "percent": (mem_used / mem_total) * 100
                    }
                }
        except Exception:
            pass
        
        return {
            "temperature": 0,
            "utilization": 0,
            "memory": {
                "used": 0,
                "total": 0,
                "percent": 0
            }
        }

    def cleanup_gpu_memory(self):
        """Force GPU memory cleanup"""
        try:
            subprocess.run(['nvidia-smi', '--gpu-reset'], check=True)
            return {"success": True, "message": "GPU memory cleaned successfully"}
        except subprocess.CalledProcessError as e:
            return {"success": False, "message": f"Failed to clean GPU memory: {str(e)}"}

    def save_metrics(self, metrics: Dict[str, Any], file_path: str = "metrics.json"):
        """Save metrics to file"""
        metrics_file = Path(file_path)
        metrics_file.parent.mkdir(parents=True, exist_ok=True)
        with open(metrics_file, 'w') as f:
            json.dump(metrics, f, indent=4)
