"""
Visualization components for agent system
"""
import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from typing import Dict, List, Any
from datetime import datetime, timedelta
import json

class AgentNetworkVisualizer:
    def __init__(self, master):
        self.master = master
        self.figure, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def update_network(self, agent_system):
        """Update the agent network visualization"""
        self.ax.clear()
        G = nx.DiGraph()
        
        def add_agent_to_graph(agent, parent_id=None):
            G.add_node(
                agent.id,
                role=agent.role.value,
                tasks=len(agent.tasks)
            )
            if parent_id:
                G.add_edge(parent_id, agent.id)
            for subordinate in agent.subordinates:
                add_agent_to_graph(subordinate, agent.id)
                
        add_agent_to_graph(agent_system.director)
        
        # Set node colors based on role
        colors = {
            'director': 'red',
            'sub_director': 'orange',
            'manager': 'green',
            'agent': 'blue'
        }
        
        node_colors = [colors[G.nodes[node]['role']] for node in G.nodes()]
        
        # Draw the network
        pos = nx.spring_layout(G)
        nx.draw(
            G,
            pos,
            ax=self.ax,
            node_color=node_colors,
            with_labels=True,
            node_size=1000,
            font_size=8,
            font_weight='bold'
        )
        
        self.canvas.draw()

class ReconciliationVisualizer:
    def __init__(self, master):
        self.master = master
        self.frame = ttk.Frame(master)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Create tree view
        self.tree = ttk.Treeview(self.frame, height=10)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            self.frame,
            orient=tk.VERTICAL,
            command=self.tree.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Configure columns
        self.tree["columns"] = ("agent", "result", "status")
        self.tree.column("#0", width=100, minwidth=100)
        self.tree.column("agent", width=150, minwidth=150)
        self.tree.column("result", width=300, minwidth=300)
        self.tree.column("status", width=100, minwidth=100)
        
        # Configure headers
        self.tree.heading("#0", text="Round")
        self.tree.heading("agent", text="Agent")
        self.tree.heading("result", text="Result")
        self.tree.heading("status", text="Status")
        
    def update_reconciliation(self, reconciliation_data: Dict):
        """Update the reconciliation visualization"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Add new data
        for round_num, round_data in enumerate(reconciliation_data['rounds'], 1):
            round_id = self.tree.insert(
                "",
                'end',
                text=f"Round {round_num}",
                values=("", "", "")
            )
            
            for agent_id, result in round_data['results'].items():
                status = "Matched" if result['matched'] else "Differed"
                self.tree.insert(
                    round_id,
                    'end',
                    text="",
                    values=(
                        agent_id,
                        json.dumps(result['data'], indent=2),
                        status
                    )
                )

class ActivityVisualizer:
    def __init__(self, master):
        self.master = master
        self.frame = ttk.Frame(master)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Create filters
        filter_frame = ttk.LabelFrame(self.frame, text="Filters")
        filter_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Agent filter
        ttk.Label(filter_frame, text="Agent:").grid(row=0, column=0, padx=5, pady=2)
        self.agent_var = tk.StringVar()
        self.agent_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.agent_var
        )
        self.agent_combo.grid(row=0, column=1, padx=5, pady=2)
        
        # Activity type filter
        ttk.Label(filter_frame, text="Activity:").grid(row=0, column=2, padx=5, pady=2)
        self.activity_var = tk.StringVar()
        self.activity_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.activity_var
        )
        self.activity_combo.grid(row=0, column=3, padx=5, pady=2)
        
        # Status filter
        ttk.Label(filter_frame, text="Status:").grid(row=0, column=4, padx=5, pady=2)
        self.status_var = tk.StringVar()
        self.status_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.status_var,
            values=["All", "success", "error"]
        )
        self.status_combo.grid(row=0, column=5, padx=5, pady=2)
        
        # Create activity list
        self.tree = ttk.Treeview(self.frame, height=10)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            self.frame,
            orient=tk.VERTICAL,
            command=self.tree.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Configure columns
        self.tree["columns"] = ("timestamp", "agent", "activity", "status", "details")
        self.tree.column("#0", width=50, minwidth=50)
        self.tree.column("timestamp", width=150, minwidth=150)
        self.tree.column("agent", width=100, minwidth=100)
        self.tree.column("activity", width=100, minwidth=100)
        self.tree.column("status", width=80, minwidth=80)
        self.tree.column("details", width=300, minwidth=300)
        
        # Configure headers
        self.tree.heading("#0", text="#")
        self.tree.heading("timestamp", text="Timestamp")
        self.tree.heading("agent", text="Agent")
        self.tree.heading("activity", text="Activity")
        self.tree.heading("status", text="Status")
        self.tree.heading("details", text="Details")
        
        # Bind filter changes
        self.agent_combo.bind('<<ComboboxSelected>>', self.apply_filters)
        self.activity_combo.bind('<<ComboboxSelected>>', self.apply_filters)
        self.status_combo.bind('<<ComboboxSelected>>', self.apply_filters)
        
    def update_activities(self, activities: List[Dict[str, Any]]):
        """Update the activity visualization"""
        # Update filter options
        agents = set()
        activity_types = set()
        
        for activity in activities:
            agents.add(activity['agent_id'])
            activity_types.add(activity['activity_type'])
            
        self.agent_combo['values'] = ["All"] + list(sorted(agents))
        self.activity_combo['values'] = ["All"] + list(sorted(activity_types))
        
        self.apply_filters(None)
        
    def apply_filters(self, event):
        """Apply filters to activity list"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Get filter values
        agent_filter = self.agent_var.get()
        activity_filter = self.activity_var.get()
        status_filter = self.status_var.get()
        
        # Add filtered activities
        for i, activity in enumerate(self.activities, 1):
            if agent_filter != "All" and activity['agent_id'] != agent_filter:
                continue
                
            if activity_filter != "All" and activity['activity_type'] != activity_filter:
                continue
                
            if status_filter != "All" and activity['status'] != status_filter:
                continue
                
            self.tree.insert(
                "",
                'end',
                text=str(i),
                values=(
                    activity['timestamp'],
                    activity['agent_id'],
                    activity['activity_type'],
                    activity['status'],
                    json.dumps(activity['details'], indent=2)
                )
            )
