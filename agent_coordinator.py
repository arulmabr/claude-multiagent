#!/usr/bin/env python3
"""
Agent Coordination System
Helps multiple AI agents coordinate through shared state
"""

import json
import time
from datetime import datetime
from pathlib import Path

STATE_FILE = Path(__file__).parent / "state" / "shared.json"


def read_state():
    """Read current shared state"""
    with open(STATE_FILE, 'r') as f:
        return json.load(f)


def write_state(state):
    """Write updated shared state"""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)


def register_agent(agent_id, role="worker", capabilities=None):
    """Register a new agent in the system"""
    state = read_state()

    if capabilities is None:
        capabilities = []

    state["agents"][agent_id] = {
        "id": agent_id,
        "registered_at": int(time.time()),
        "status": "active",
        "role": role,
        "capabilities": capabilities,
        "last_seen": int(time.time())
    }

    write_state(state)
    print(f"Agent {agent_id} registered successfully")


def send_message(from_agent, content):
    """Send a message to other agents"""
    state = read_state()

    message = {
        "from": from_agent,
        "timestamp": int(time.time()),
        "content": content
    }

    state["messages"].append(message)
    write_state(state)
    print(f"Message sent from {from_agent}")


def get_messages(since_timestamp=0):
    """Get messages since a specific timestamp"""
    state = read_state()
    return [msg for msg in state["messages"] if msg["timestamp"] > since_timestamp]


def get_active_agents():
    """Get list of currently active agents"""
    state = read_state()
    return list(state["agents"].keys())


def add_observation(agent_id, observation):
    """Add an observation to shared memory"""
    state = read_state()

    obs_entry = f"{agent_id}: {observation}"
    if "observations" not in state["memory"]:
        state["memory"]["observations"] = []

    state["memory"]["observations"].append(obs_entry)
    write_state(state)


def update_coordination(updates):
    """Update coordination section with new information"""
    state = read_state()
    state["coordination"].update(updates)
    write_state(state)


def heartbeat(agent_id):
    """Update agent's last_seen timestamp"""
    state = read_state()
    if agent_id in state["agents"]:
        state["agents"][agent_id]["last_seen"] = int(time.time())
        write_state(state)


if __name__ == "__main__":
    print("Agent Coordination System")
    print("=" * 50)

    state = read_state()
    print(f"\nActive Agents: {len(state['agents'])}")
    for agent_id, info in state['agents'].items():
        print(f"  - {agent_id} ({info['role']})")

    print(f"\nMessages: {len(state['messages'])}")
    for msg in state['messages'][-5:]:  # Show last 5 messages
        print(f"  [{msg['from']}]: {msg['content']}")

    print(f"\nObservations: {len(state.get('memory', {}).get('observations', []))}")
