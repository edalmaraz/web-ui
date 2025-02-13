"""
Advanced logging system for agent activities
"""
import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class AgentActivity:
    timestamp: str
    agent_id: str
    agent_role: str
    activity_type: str
    details: Dict[str, Any]
    task_id: Optional[str] = None
    status: str = "success"
    error: Optional[str] = None

class AgentLogger:
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up file handler
        self.setup_file_logger()
        
        # In-memory activity store
        self.activities = []
        
    def setup_file_logger(self):
        """Set up file-based logging"""
        self.logger = logging.getLogger("agent_system")
        self.logger.setLevel(logging.DEBUG)
        
        # Create handlers
        file_handler = logging.FileHandler(
            self.log_dir / f"agent_activity_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )
        console_handler = logging.StreamHandler()
        
        # Create formatters
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
        
        # Set formatters
        file_handler.setFormatter(file_formatter)
        console_handler.setFormatter(console_formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
    def log_activity(
        self,
        agent_id: str,
        agent_role: str,
        activity_type: str,
        details: Dict[str, Any],
        task_id: Optional[str] = None,
        status: str = "success",
        error: Optional[str] = None
    ):
        """Log an agent activity"""
        activity = AgentActivity(
            timestamp=datetime.now().isoformat(),
            agent_id=agent_id,
            agent_role=agent_role,
            activity_type=activity_type,
            details=details,
            task_id=task_id,
            status=status,
            error=error
        )
        
        # Store in memory
        self.activities.append(activity)
        
        # Log to file
        log_message = (
            f"Agent: {agent_id} ({agent_role}) - "
            f"Activity: {activity_type} - "
            f"Status: {status}"
        )
        
        if task_id:
            log_message += f" - Task: {task_id}"
            
        if error:
            log_message += f" - Error: {error}"
            self.logger.error(log_message)
        else:
            self.logger.info(log_message)
            
        # Log details at debug level
        self.logger.debug(f"Details: {json.dumps(details, indent=2)}")
        
    def get_activities(
        self,
        agent_id: Optional[str] = None,
        activity_type: Optional[str] = None,
        task_id: Optional[str] = None,
        status: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> list:
        """Get filtered activities"""
        filtered = self.activities
        
        if agent_id:
            filtered = [a for a in filtered if a.agent_id == agent_id]
            
        if activity_type:
            filtered = [a for a in filtered if a.activity_type == activity_type]
            
        if task_id:
            filtered = [a for a in filtered if a.task_id == task_id]
            
        if status:
            filtered = [a for a in filtered if a.status == status]
            
        if start_time:
            filtered = [
                a for a in filtered
                if datetime.fromisoformat(a.timestamp) >= start_time
            ]
            
        if end_time:
            filtered = [
                a for a in filtered
                if datetime.fromisoformat(a.timestamp) <= end_time
            ]
            
        return filtered
        
    def export_activities(self, filepath: Optional[str] = None) -> str:
        """Export activities to JSON file"""
        if not filepath:
            filepath = self.log_dir / f"activities_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
        activities_dict = [asdict(a) for a in self.activities]
        
        with open(filepath, 'w') as f:
            json.dump(activities_dict, f, indent=2)
            
        return filepath
        
    def clear_activities(self):
        """Clear in-memory activities"""
        self.activities = []

# Global logger instance
agent_logger = AgentLogger()
