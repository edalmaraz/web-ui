"""
Tests for the UI components
"""
import pytest
import tkinter as tk
from src.agents.agent_manager_ui import AgentManagerUI
from src.agents.visualization import (
    AgentNetworkVisualizer,
    ReconciliationVisualizer,
    ActivityVisualizer
)

@pytest.fixture
def root():
    """Create a test Tk root"""
    root = tk.Tk()
    yield root
    root.destroy()

def test_agent_manager_ui_creation(root):
    """Test UI creation"""
    ui = AgentManagerUI(root)
    
    # Check main components
    assert ui.notebook is not None
    assert len(ui.notebook.tabs()) == 5  # Control, Task, Viz, Activity, Reconciliation
    
    # Check variables
    assert isinstance(ui.double_check_mode, tk.BooleanVar)
    assert isinstance(ui.hierarchy_mode, tk.BooleanVar)
    
    # Check task variables
    assert isinstance(ui.complexity_var, tk.IntVar)
    assert isinstance(ui.scope_var, tk.IntVar)
    assert isinstance(ui.urgency_var, tk.IntVar)
    assert isinstance(ui.task_type_var, tk.StringVar)
    assert isinstance(ui.priority_var, tk.StringVar)
    assert isinstance(ui.timeout_var, tk.IntVar)

def test_visualization_components(root):
    """Test visualization components"""
    # Network visualizer
    network_viz = AgentNetworkVisualizer(root)
    assert network_viz.canvas is not None
    assert network_viz.figure is not None
    assert network_viz.ax is not None
    
    # Activity visualizer
    activity_viz = ActivityVisualizer(root)
    assert activity_viz.tree is not None
    assert activity_viz.agent_combo is not None
    assert activity_viz.activity_combo is not None
    assert activity_viz.status_combo is not None
    
    # Reconciliation visualizer
    reconciliation_viz = ReconciliationVisualizer(root)
    assert reconciliation_viz.tree is not None

def test_ui_mode_toggles(root):
    """Test UI mode toggles"""
    ui = AgentManagerUI(root)
    
    # Test hierarchy mode
    ui.hierarchy_mode.set(True)
    ui.toggle_hierarchy()
    assert ui.agent_system is not None
    
    ui.hierarchy_mode.set(False)
    ui.toggle_hierarchy()
    assert ui.agent_system is None
    
    # Test double-check mode
    ui.hierarchy_mode.set(True)
    ui.toggle_hierarchy()
    ui.double_check_mode.set(True)
    ui.toggle_double_check()
    assert ui.agent_system.double_check_mode is True

def test_task_configuration(root):
    """Test task configuration"""
    ui = AgentManagerUI(root)
    
    # Set task parameters
    ui.complexity_var.set(5)
    ui.scope_var.set(5)
    ui.urgency_var.set(5)
    ui.task_type_var.set("data_analysis")
    ui.priority_var.set("high")
    ui.timeout_var.set(120)
    
    # Enable system
    ui.hierarchy_mode.set(True)
    ui.toggle_hierarchy()
    
    # Update preview
    ui.update_preview()
    
    # Check preview content
    preview_text = ui.preview_text.get("1.0", tk.END)
    assert "Task Type: data_analysis" in preview_text
    assert "Priority: high" in preview_text
    assert "Timeout: 120s" in preview_text
