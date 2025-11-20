#!/usr/bin/env python3
"""
Agent Discovery - Monitor and detect other agents in the system.
"""

import json
import os
from timestamp_utils import get_timestamp, time_since, format_duration

STATE_FILE = "state/shared.json"

class AgentDiscovery:
    def __init__(self, my_agent_id):
        self.my_id = my_agent_id
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

    def heartbeat(self):
        """Update agent's last_seen timestamp."""
        state = self.read_state()

        if self.my_id in state["agents"]:
            state["agents"][self.my_id]["last_seen"] = get_timestamp()
            self.write_state(state)

    def list_agents(self, active_only=True):
        """List all agents, optionally filtering to only active ones."""
        state = self.read_state()
        agents = state.get("agents", {})

        if active_only:
            # Consider agents active if seen in last 5 minutes
            active_agents = {}
            for agent_id, agent_data in agents.items():
                last_seen = agent_data.get("last_seen", agent_data.get("joined_at"))
                if last_seen:
                    try:
                        elapsed = time_since(last_seen)
                        if elapsed < 300:  # 5 minutes
                            active_agents[agent_id] = agent_data
                    except:
                        # If timestamp parsing fails, include the agent
                        active_agents[agent_id] = agent_data
            return active_agents
        return agents

    def detect_new_agents(self):
        """Detect if new agents have joined since last check."""
        state = self.read_state()
        current_agents = set(state.get("agents", {}).keys())

        # Update memory with current agent count
        if "known_agents" not in state["memory"]:
            state["memory"]["known_agents"] = list(current_agents)
            self.write_state(state)
            return []

        known_agents = set(state["memory"]["known_agents"])
        new_agents = current_agents - known_agents

        if new_agents:
            state["memory"]["known_agents"] = list(current_agents)
            self.write_state(state)

        return list(new_agents)

    def send_greeting(self, to_agent_id):
        """Send a greeting message to another agent."""
        state = self.read_state()

        greeting = {
            "from": self.my_id,
            "to": to_agent_id,
            "timestamp": get_timestamp(),
            "text": f"Hello {to_agent_id}! I'm {self.my_id}. Ready to collaborate!"
        }

        state["messages"].append(greeting)
        self.write_state(state)

    def get_messages_for_me(self):
        """Get messages addressed to this agent."""
        state = self.read_state()
        messages = state.get("messages", [])

        my_messages = [
            msg for msg in messages
            if msg.get("to") == self.my_id or msg.get("to") is None
        ]

        return my_messages

if __name__ == "__main__":
    # Monitor for other agents
    discovery = AgentDiscovery("gamma")

    print("🔍 Agent Discovery System")
    print("=" * 50)

    # Update heartbeat
    discovery.heartbeat()

    # List active agents
    agents = discovery.list_agents()
    print(f"\n📊 Active Agents: {len(agents)}")
    for agent_id, agent_data in agents.items():
        role = agent_data.get("role", "unknown")
        last_seen = agent_data.get("last_seen", agent_data.get("joined_at", "unknown"))
        print(f"  • {agent_id} ({role}) - last seen: {last_seen}")

    # Check for new agents
    new_agents = discovery.detect_new_agents()
    if new_agents:
        print(f"\n🎉 New agents detected: {', '.join(new_agents)}")
        for agent_id in new_agents:
            discovery.send_greeting(agent_id)
            print(f"  → Sent greeting to {agent_id}")
    else:
        print("\n⏳ No new agents detected. Waiting for others to join...")

    # Check messages
    messages = discovery.get_messages_for_me()
    if messages:
        print(f"\n📬 Messages for gamma: {len(messages)}")
        for msg in messages[-5:]:  # Show last 5
            print(f"  From {msg.get('from', 'unknown')}: {msg.get('text', '')}")
    else:
        print("\n📭 No messages yet.")
