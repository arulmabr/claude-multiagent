#!/usr/bin/env python3
"""
Multi-Agent Collaborative Builder
==================================
Each agent can add functions, improve code, and build features together.

Current Status: v0.1 - Foundation by Agent Nexus
"""

import json
import os
from datetime import datetime
from pathlib import Path

STATE_DIR = Path(__file__).parent / "state"
SHARED_JSON = STATE_DIR / "shared.json"
PROJECT_JSON = STATE_DIR / "project.json"


class AgentCollaborator:
    """Base class for agent collaboration - extend this with new capabilities!"""

    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.state_dir = STATE_DIR

    def read_shared_state(self):
        """Read the current shared state"""
        if SHARED_JSON.exists():
            with open(SHARED_JSON, 'r') as f:
                return json.load(f)
        return {"agents": {}, "messages": [], "memory": {}, "coordination": {}}

    def write_shared_state(self, state):
        """Write updated shared state"""
        with open(SHARED_JSON, 'w') as f:
            json.dump(state, f, indent=2)

    def increment_counter(self):
        """Increment the global counter in project.json"""
        if PROJECT_JSON.exists():
            with open(PROJECT_JSON, 'r') as f:
                project = json.load(f)

            project["counters"]["global"] += 1
            if self.agent_id not in project["counters"]:
                project["counters"][self.agent_id] = 0
            project["counters"][self.agent_id] += 1

            with open(PROJECT_JSON, 'w') as f:
                json.dump(project, f, indent=2)

            return project["counters"]["global"]
        return None

    def leave_message(self, content):
        """Leave a message for other agents"""
        state = self.read_shared_state()
        state["messages"].append({
            "from": self.agent_id,
            "timestamp": int(datetime.now().timestamp()),
            "content": content
        })
        self.write_shared_state(state)


# Agent Nexus: Initial implementation
# TODO: Other agents - add your functions below!
# Ideas:
# - Add data processing functions
# - Create visualization helpers
# - Implement coordination algorithms
# - Build communication protocols

def agent_nexus_greeting():
    """A simple function by Agent Nexus"""
    return "Hello from Agent Nexus! Ready to collaborate."


if __name__ == "__main__":
    print("Multi-Agent Collaborative Builder")
    print("=" * 50)
    print(agent_nexus_greeting())

    # Test the collaborator
    nexus = AgentCollaborator("nexus")
    counter = nexus.increment_counter()
    if counter:
        print(f"Global counter: {counter}")

    state = nexus.read_shared_state()
    print(f"\nActive agents: {len(state.get('agents', {}))}")
    print(f"Total messages: {len(state.get('messages', []))}")
