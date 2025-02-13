"""
Hierarchical Agent Management System
"""
import asyncio
import json
import uuid
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

class AgentRole(Enum):
    DIRECTOR = "director"
    SUB_DIRECTOR = "sub_director"
    MANAGER = "manager"
    AGENT = "agent"

@dataclass
class AgentTask:
    id: str
    description: str
    status: str
    assigned_to: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    result: Any = None
    verification_status: str = "pending"
    verification_result: Optional[Dict] = None

class Agent:
    def __init__(self, agent_id: str, role: AgentRole):
        self.id = agent_id
        self.role = role
        self.tasks: List[AgentTask] = []
        self.subordinates: List[Agent] = []
        self.superior: Optional[Agent] = None
        self.current_task: Optional[AgentTask] = None
        
    async def process_task(self, task: AgentTask) -> Dict:
        """Process a task and return results"""
        raise NotImplementedError
        
    def add_subordinate(self, agent: 'Agent'):
        """Add a subordinate agent"""
        self.subordinates.append(agent)
        agent.superior = self
        
    def report_status(self) -> Dict:
        """Report agent status and subordinates"""
        return {
            'id': self.id,
            'role': self.role.value,
            'current_task': self.current_task.id if self.current_task else None,
            'subordinates': len(self.subordinates),
            'tasks_completed': len([t for t in self.tasks if t.completed_at]),
            'tasks_pending': len([t for t in self.tasks if not t.completed_at])
        }

class Director(Agent):
    def __init__(self, agent_id: str):
        super().__init__(agent_id, AgentRole.DIRECTOR)
        self.sub_directors: List[SubDirector] = []
        
    async def analyze_task(self, task: Dict) -> Dict:
        """Analyze task and determine required resources"""
        complexity = task.get('complexity', 1)
        scope = task.get('scope', 1)
        urgency = task.get('urgency', 1)
        
        # Calculate required resources
        sub_directors = 2  # Fixed as per requirement
        managers_per_sub = max(1, (complexity * scope) // 3)
        agents_per_manager = max(2, (complexity * scope * urgency) // 2)
        
        return {
            'sub_directors': sub_directors,
            'managers_per_sub': managers_per_sub,
            'agents_per_manager': agents_per_manager,
            'total_managers': sub_directors * managers_per_sub,
            'total_agents': sub_directors * managers_per_sub * agents_per_manager
        }
        
    async def delegate_task(self, task: Dict) -> Dict:
        """Delegate task to sub-directors"""
        resources = await self.analyze_task(task)
        
        # Create sub-directors if needed
        while len(self.sub_directors) < 2:
            sub_director = SubDirector(f"sub_director_{len(self.sub_directors)}")
            self.add_subordinate(sub_director)
            self.sub_directors.append(sub_director)
        
        # Split task between sub-directors
        results = await asyncio.gather(
            *[sub.handle_task(task, resources) for sub in self.sub_directors]
        )
        
        return {
            'resources': resources,
            'sub_director_results': results
        }

class SubDirector(Agent):
    def __init__(self, agent_id: str):
        super().__init__(agent_id, AgentRole.SUB_DIRECTOR)
        self.managers: List[Manager] = []
        
    async def handle_task(self, task: Dict, resources: Dict) -> Dict:
        """Handle task delegation to managers"""
        # Create required managers
        managers_needed = resources['managers_per_sub']
        while len(self.managers) < managers_needed:
            manager = Manager(f"manager_{self.id}_{len(self.managers)}")
            self.add_subordinate(manager)
            self.managers.append(manager)
        
        # Delegate to managers
        results = await asyncio.gather(
            *[manager.handle_task(task, resources) for manager in self.managers]
        )
        
        return {
            'manager_count': len(self.managers),
            'results': results
        }

class Manager(Agent):
    def __init__(self, agent_id: str):
        super().__init__(agent_id, AgentRole.MANAGER)
        self.agents: List[WorkerAgent] = []
        
    async def handle_task(self, task: Dict, resources: Dict) -> Dict:
        """Handle task delegation to agents"""
        # Create required agents
        agents_needed = resources['agents_per_manager']
        while len(self.agents) < agents_needed:
            agent = WorkerAgent(f"agent_{self.id}_{len(self.agents)}")
            self.add_subordinate(agent)
            self.agents.append(agent)
        
        # Delegate to agents
        results = await asyncio.gather(
            *[agent.process_task(task) for agent in self.agents]
        )
        
        return {
            'agent_count': len(self.agents),
            'results': results
        }

class WorkerAgent(Agent):
    def __init__(self, agent_id: str):
        super().__init__(agent_id, AgentRole.AGENT)
        
    async def process_task(self, task: Dict) -> Dict:
        """Process the actual task"""
        # Implement actual task processing logic
        result = await self._execute_task(task)
        return {
            'agent_id': self.id,
            'task_id': task['id'],
            'result': result
        }
        
    async def _execute_task(self, task: Dict) -> Any:
        """Execute the task and return result"""
        # Implement specific task execution logic
        pass

class AgentSystem:
    def __init__(self, double_check_mode: bool = False):
        self.director = Director("main_director")
        self.double_check_mode = double_check_mode
        self.task_results: Dict[str, List[Dict]] = {}
        
    async def process_task(self, task: Dict) -> Dict:
        """Process a task through the agent hierarchy"""
        task_id = str(uuid.uuid4())
        task['id'] = task_id
        
        # Get results from director
        results = await self.director.delegate_task(task)
        
        if self.double_check_mode:
            # Compare results from different agents
            agent_results = self._extract_agent_results(results)
            self.task_results[task_id] = agent_results
            
            if not self._results_match(agent_results):
                # Trigger reconciliation
                reconciled_results = await self._reconcile_results(task_id, agent_results)
                results['reconciled_results'] = reconciled_results
        
        return results
        
    def _extract_agent_results(self, results: Dict) -> List[Dict]:
        """Extract individual agent results from the hierarchy"""
        agent_results = []
        for sub_dir_result in results['sub_director_results']:
            for manager_result in sub_dir_result['results']:
                agent_results.extend(manager_result['results'])
        return agent_results
        
    def _results_match(self, results: List[Dict]) -> bool:
        """Check if all agent results match"""
        if not results:
            return True
        first_result = json.dumps(results[0]['result'], sort_keys=True)
        return all(json.dumps(r['result'], sort_keys=True) == first_result 
                  for r in results)
        
    async def _reconcile_results(
        self,
        task_id: str,
        results: List[Dict]
    ) -> Dict:
        """Reconcile different results through agent collaboration"""
        # Group agents by their results
        result_groups = {}
        for result in results:
            result_key = json.dumps(result['result'], sort_keys=True)
            if result_key not in result_groups:
                result_groups[result_key] = []
            result_groups[result_key].append(result['agent_id'])
        
        if len(result_groups) > 1:
            # Create a reconciliation task
            reconciliation_task = {
                'id': f"reconcile_{task_id}",
                'type': 'reconciliation',
                'different_results': result_groups,
                'original_task_id': task_id
            }
            
            # Process reconciliation through the hierarchy again
            reconciled_results = await self.process_task(reconciliation_task)
            return reconciled_results
        
        return {'status': 'matched', 'result': results[0]['result']}
