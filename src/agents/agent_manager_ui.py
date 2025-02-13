"""
Enhanced Agent Management System UI
"""
import tkinter as tk
from tkinter import ttk
import json
from typing import Dict, Optional
from datetime import datetime, timedelta
from .agent_hierarchy import AgentSystem
from .agent_logging import agent_logger
from .visualization import (
    AgentNetworkVisualizer,
    ReconciliationVisualizer,
    ActivityVisualizer
)
from .specialized_agents import create_specialized_agent

class AgentManagerUI:
    def __init__(self, root: Optional[tk.Tk] = None):
        self.root = root or tk.Tk()
        self.root.title("Agent Management System")
        
        # Initialize agent system
        self.agent_system = None
        self.double_check_mode = tk.BooleanVar(value=False)
        self.hierarchy_mode = tk.BooleanVar(value=False)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create tabs
        self.create_control_tab()
        self.create_task_tab()
        self.create_visualization_tab()
        self.create_activity_tab()
        self.create_reconciliation_tab()
        
    def create_control_tab(self):
        """Create the main control tab"""
        control_frame = ttk.Frame(self.notebook)
        self.notebook.add(control_frame, text="Control")
        
        # Mode Selection
        mode_frame = ttk.LabelFrame(control_frame, text="System Configuration", padding="5")
        mode_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Checkbutton(
            mode_frame,
            text="Enable Hierarchical Management",
            variable=self.hierarchy_mode,
            command=self.toggle_hierarchy
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        ttk.Checkbutton(
            mode_frame,
            text="Enable Double-Check Mode",
            variable=self.double_check_mode,
            command=self.toggle_double_check
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Status Display
        self.status_frame = ttk.LabelFrame(control_frame, text="System Status", padding="5")
        self.status_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create status display
        self.create_status_display()
        
    def create_task_tab(self):
        """Create the task configuration tab"""
        task_frame = ttk.Frame(self.notebook)
        self.notebook.add(task_frame, text="Task Configuration")
        
        # Basic Parameters
        basic_frame = ttk.LabelFrame(task_frame, text="Basic Parameters", padding="5")
        basic_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Complexity
        ttk.Label(basic_frame, text="Task Complexity:").grid(row=0, column=0, padx=5, pady=2)
        self.complexity_var = tk.IntVar(value=1)
        complexity_scale = ttk.Scale(
            basic_frame,
            from_=1,
            to=10,
            variable=self.complexity_var,
            orient=tk.HORIZONTAL
        )
        complexity_scale.grid(row=0, column=1, padx=5, pady=2, sticky=(tk.W, tk.E))
        
        # Scope
        ttk.Label(basic_frame, text="Task Scope:").grid(row=1, column=0, padx=5, pady=2)
        self.scope_var = tk.IntVar(value=1)
        scope_scale = ttk.Scale(
            basic_frame,
            from_=1,
            to=10,
            variable=self.scope_var,
            orient=tk.HORIZONTAL
        )
        scope_scale.grid(row=1, column=1, padx=5, pady=2, sticky=(tk.W, tk.E))
        
        # Urgency
        ttk.Label(basic_frame, text="Task Urgency:").grid(row=2, column=0, padx=5, pady=2)
        self.urgency_var = tk.IntVar(value=1)
        urgency_scale = ttk.Scale(
            basic_frame,
            from_=1,
            to=10,
            variable=self.urgency_var,
            orient=tk.HORIZONTAL
        )
        urgency_scale.grid(row=2, column=1, padx=5, pady=2, sticky=(tk.W, tk.E))
        
        # Advanced Parameters
        advanced_frame = ttk.LabelFrame(task_frame, text="Advanced Parameters", padding="5")
        advanced_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Task Type
        ttk.Label(advanced_frame, text="Task Type:").grid(row=0, column=0, padx=5, pady=2)
        self.task_type_var = tk.StringVar()
        task_type_combo = ttk.Combobox(
            advanced_frame,
            textvariable=self.task_type_var,
            values=[
                "data_analysis",
                "web_scraping",
                "text_processing",
                "image_processing",
                "code_analysis",
                "database",
                "api",
                "testing"
            ]
        )
        task_type_combo.grid(row=0, column=1, padx=5, pady=2)
        
        # Priority
        ttk.Label(advanced_frame, text="Priority:").grid(row=1, column=0, padx=5, pady=2)
        self.priority_var = tk.StringVar(value="medium")
        priority_combo = ttk.Combobox(
            advanced_frame,
            textvariable=self.priority_var,
            values=["low", "medium", "high", "critical"]
        )
        priority_combo.grid(row=1, column=1, padx=5, pady=2)
        
        # Timeout
        ttk.Label(advanced_frame, text="Timeout (s):").grid(row=2, column=0, padx=5, pady=2)
        self.timeout_var = tk.IntVar(value=60)
        timeout_spin = ttk.Spinbox(
            advanced_frame,
            from_=1,
            to=3600,
            textvariable=self.timeout_var
        )
        timeout_spin.grid(row=2, column=1, padx=5, pady=2)
        
        # Resource Preview
        preview_frame = ttk.LabelFrame(task_frame, text="Resource Preview", padding="5")
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.preview_text = tk.Text(preview_frame, height=10, width=50)
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Update button
        ttk.Button(
            task_frame,
            text="Update Preview",
            command=self.update_preview
        ).pack(pady=5)
        
    def create_visualization_tab(self):
        """Create the visualization tab"""
        viz_frame = ttk.Frame(self.notebook)
        self.notebook.add(viz_frame, text="Visualization")
        
        # Create network visualizer
        self.network_viz = AgentNetworkVisualizer(viz_frame)
        
    def create_activity_tab(self):
        """Create the activity monitoring tab"""
        activity_frame = ttk.Frame(self.notebook)
        self.notebook.add(activity_frame, text="Activity Log")
        
        # Create activity visualizer
        self.activity_viz = ActivityVisualizer(activity_frame)
        
    def create_reconciliation_tab(self):
        """Create the reconciliation monitoring tab"""
        reconciliation_frame = ttk.Frame(self.notebook)
        self.notebook.add(reconciliation_frame, text="Reconciliation")
        
        # Create reconciliation visualizer
        self.reconciliation_viz = ReconciliationVisualizer(reconciliation_frame)
        
    def create_status_display(self):
        """Create the status display area"""
        # Clear existing widgets
        for widget in self.status_frame.winfo_children():
            widget.destroy()
            
        if self.agent_system:
            # Create a tree view for the agent hierarchy
            self.tree = ttk.Treeview(self.status_frame, height=6)
            self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(
                self.status_frame,
                orient=tk.VERTICAL,
                command=self.tree.yview
            )
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.tree.configure(yscrollcommand=scrollbar.set)
            
            # Configure columns
            self.tree["columns"] = ("role", "tasks", "subordinates", "type")
            self.tree.column("#0", width=120, minwidth=120)
            self.tree.column("role", width=100, minwidth=100)
            self.tree.column("tasks", width=80, minwidth=80)
            self.tree.column("subordinates", width=100, minwidth=100)
            self.tree.column("type", width=100, minwidth=100)
            
            # Configure headers
            self.tree.heading("#0", text="Agent ID")
            self.tree.heading("role", text="Role")
            self.tree.heading("tasks", text="Tasks")
            self.tree.heading("subordinates", text="Subordinates")
            self.tree.heading("type", text="Type")
            
            # Populate tree
            self.populate_agent_tree()
        else:
            ttk.Label(
                self.status_frame,
                text="Hierarchical Management Disabled"
            ).pack(padx=5, pady=5)
            
    def populate_agent_tree(self, parent="", agent=None):
        """Recursively populate the agent tree"""
        if agent is None:
            agent = self.agent_system.director
            
        # Add this agent to the tree
        status = agent.report_status()
        agent_id = status['id']
        
        agent_type = getattr(agent, 'specialization', 'general')
        
        self.tree.insert(
            parent,
            'end',
            agent_id,
            text=agent_id,
            values=(
                status['role'],
                f"{status['tasks_completed']}/{status['tasks_pending']}",
                status['subordinates'],
                agent_type
            )
        )
        
        # Add subordinates
        for subordinate in agent.subordinates:
            self.populate_agent_tree(agent_id, subordinate)
            
    def toggle_hierarchy(self):
        """Toggle hierarchical management system"""
        if self.hierarchy_mode.get():
            self.agent_system = AgentSystem(
                double_check_mode=self.double_check_mode.get()
            )
            # Update visualizations
            self.network_viz.update_network(self.agent_system)
        else:
            self.agent_system = None
            
        self.create_status_display()
        self.update_preview()
        
    def toggle_double_check(self):
        """Toggle double-check mode"""
        if self.agent_system:
            self.agent_system.double_check_mode = self.double_check_mode.get()
        self.update_preview()
        
    def update_preview(self):
        """Update the resource preview"""
        if not self.agent_system:
            preview = "Hierarchical Management Disabled"
        else:
            task = {
                'complexity': self.complexity_var.get(),
                'scope': self.scope_var.get(),
                'urgency': self.urgency_var.get(),
                'type': self.task_type_var.get(),
                'priority': self.priority_var.get(),
                'timeout': self.timeout_var.get()
            }
            
            import asyncio
            resources = asyncio.run(
                self.agent_system.director.analyze_task(task)
            )
            
            preview = "Resource Allocation:\n\n"
            preview += f"Task Type: {task['type']}\n"
            preview += f"Priority: {task['priority']}\n"
            preview += f"Timeout: {task['timeout']}s\n\n"
            preview += f"Sub-Directors: {resources['sub_directors']}\n"
            preview += f"Managers per Sub-Director: {resources['managers_per_sub']}\n"
            preview += f"Agents per Manager: {resources['agents_per_manager']}\n"
            preview += f"Total Managers: {resources['total_managers']}\n"
            preview += f"Total Agents: {resources['total_agents']}\n"
            
            if self.double_check_mode.get():
                preview += "\nDouble-Check Mode: Enabled"
                preview += "\nAll tasks will be verified by multiple agents"
            
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(tk.END, preview)
        
        # Update visualizations
        if self.agent_system:
            self.network_viz.update_network(self.agent_system)
            self.activity_viz.update_activities(agent_logger.get_activities())
            
    def run(self):
        """Start the UI"""
        self.root.mainloop()
