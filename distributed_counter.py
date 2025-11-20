"""
Distributed Counter - A simple concurrent counter for multi-agent coordination.
Each agent can increment, read, and leave a signature.
"""

import json
import os
from datetime import datetime

STATE_FILE = "state/shared.json"

class DistributedCounter:
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

    def increment_counter(self, agent_id):
        """Increment the global counter and record the agent."""
        state = self.read_state()

        # Initialize counter if it doesn't exist
        if "counter" not in state["coordination"]:
            state["coordination"]["counter"] = 0
            state["coordination"]["counter_history"] = []

        # Increment
        state["coordination"]["counter"] += 1
        state["coordination"]["counter_history"].append({
            "agent": agent_id,
            "value": state["coordination"]["counter"],
            "timestamp": datetime.now().isoformat()
        })

        self.write_state(state)
        return state["coordination"]["counter"]

    def get_counter(self):
        """Get current counter value."""
        state = self.read_state()
        return state["coordination"].get("counter", 0)

    def register_agent(self, agent_id, metadata=None):
        """Register an agent in the shared state."""
        state = self.read_state()
        state["agents"][agent_id] = {
            "id": agent_id,
            "status": "active",
            "joined_at": datetime.now().isoformat(),
            **(metadata or {})
        }
        self.write_state(state)
        return len(state["agents"])

if __name__ == "__main__":
    # Example usage
    counter = DistributedCounter()
    counter.register_agent("gamma", {"role": "coordinator"})
    count = counter.increment_counter("gamma")
    print(f"Counter: {count}")
    print(f"Total agents: {len(counter.read_state()['agents'])}")
