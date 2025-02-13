"""
Tests for the agent management system
"""
import pytest
import asyncio
from src.agents.agent_hierarchy import (
    AgentSystem,
    Director,
    SubDirector,
    Manager,
    WorkerAgent
)
from src.agents.specialized_agents import create_specialized_agent

@pytest.fixture
def agent_system():
    """Create a test agent system"""
    return AgentSystem(double_check_mode=True)

def test_agent_creation(agent_system):
    """Test agent creation and hierarchy"""
    assert isinstance(agent_system.director, Director)
    assert len(agent_system.director.sub_directors) == 0
    
    # Enable system
    agent_system.hierarchy_mode = True
    assert len(agent_system.director.sub_directors) == 2
    
    for sub_director in agent_system.director.sub_directors:
        assert isinstance(sub_director, SubDirector)
        assert sub_director.superior == agent_system.director

@pytest.mark.asyncio
async def test_task_delegation(agent_system):
    """Test task delegation through hierarchy"""
    task = {
        'id': 'test_task',
        'complexity': 5,
        'scope': 5,
        'urgency': 5,
        'type': 'data_analysis'
    }
    
    # Enable system
    agent_system.hierarchy_mode = True
    
    # Process task
    results = await agent_system.process_task(task)
    
    assert 'resources' in results
    assert 'sub_director_results' in results
    assert len(results['sub_director_results']) == 2

def test_specialized_agents():
    """Test specialized agent creation"""
    agent_types = [
        "data_analysis",
        "web_scraping",
        "text_processing",
        "image_processing",
        "code_analysis",
        "database",
        "api",
        "testing"
    ]
    
    for agent_type in agent_types:
        agent = create_specialized_agent(agent_type, f"test_{agent_type}")
        assert agent.specialization == agent_type
        assert isinstance(agent, WorkerAgent)

@pytest.mark.asyncio
async def test_double_check_mode(agent_system):
    """Test double-check mode reconciliation"""
    task = {
        'id': 'test_task',
        'complexity': 3,
        'scope': 3,
        'urgency': 3,
        'type': 'data_analysis'
    }
    
    # Enable system and double-check mode
    agent_system.hierarchy_mode = True
    agent_system.double_check_mode = True
    
    # Process task
    results = await agent_system.process_task(task)
    
    # Verify double-check results
    assert 'reconciled_results' in results
