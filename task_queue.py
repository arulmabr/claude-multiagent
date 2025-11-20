"""
Distributed Task Queue - For multi-agent coordination.
Agents can add tasks, claim tasks, and complete tasks.
"""

import json
import os
from datetime import datetime

STATE_FILE = "state/shared.json"

class TaskQueue:
    def __init__(self):
        self.state_file = STATE_FILE

    def read_state(self):
        """Read current shared state."""
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {"agents": {}, "messages": [], "memory": {}, "coordination": {}}

    def write_state(self, state):
        """Write state back to file."""
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)

    def add_task(self, task_description, added_by, priority="normal"):
        """Add a new task to the queue."""
        state = self.read_state()

        if "tasks" not in state["coordination"]:
            state["coordination"]["tasks"] = []

        task_id = len(state["coordination"]["tasks"]) + 1
        task = {
            "id": task_id,
            "description": task_description,
            "status": "pending",
            "added_by": added_by,
            "added_at": datetime.now().isoformat(),
            "priority": priority,
            "claimed_by": None,
            "completed_by": None,
            "completed_at": None
        }

        state["coordination"]["tasks"].append(task)
        self.write_state(state)
        return task_id

    def claim_task(self, task_id, agent_id):
        """Claim a task."""
        state = self.read_state()

        if "tasks" not in state["coordination"]:
            return False

        for task in state["coordination"]["tasks"]:
            if task["id"] == task_id and task["status"] == "pending":
                task["status"] = "in_progress"
                task["claimed_by"] = agent_id
                task["claimed_at"] = datetime.now().isoformat()
                self.write_state(state)
                return True

        return False

    def complete_task(self, task_id, agent_id):
        """Mark a task as completed."""
        state = self.read_state()

        if "tasks" not in state["coordination"]:
            return False

        for task in state["coordination"]["tasks"]:
            if task["id"] == task_id and task["claimed_by"] == agent_id:
                task["status"] = "completed"
                task["completed_by"] = agent_id
                task["completed_at"] = datetime.now().isoformat()
                self.write_state(state)
                return True

        return False

    def list_tasks(self, status=None):
        """List all tasks, optionally filtered by status."""
        state = self.read_state()
        tasks = state["coordination"].get("tasks", [])

        if status:
            tasks = [t for t in tasks if t["status"] == status]

        return tasks

if __name__ == "__main__":
    # Example usage
    queue = TaskQueue()

    # Add some initial tasks for agents to work on
    queue.add_task("Create a message board module", "gamma", "high")
    queue.add_task("Implement agent discovery mechanism", "gamma", "high")
    queue.add_task("Add timestamp utilities", "gamma", "normal")
    queue.add_task("Create visualization of agent activity", "gamma", "low")

    print("Tasks added:")
    for task in queue.list_tasks():
        print(f"  [{task['id']}] {task['description']} (priority: {task['priority']})")
