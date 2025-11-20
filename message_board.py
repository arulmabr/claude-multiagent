"""
Message Board - A collaborative communication system for multi-agent coordination.
Agents can post messages, read broadcasts, and coordinate activities.
"""

import json
import os
from datetime import datetime

STATE_FILE = "state/shared.json"

class MessageBoard:
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

    def post_message(self, agent_id, text, priority="normal", tags=None):
        """Post a message to the shared message board."""
        state = self.read_state()

        # Ensure messages list exists
        if "messages" not in state:
            state["messages"] = []

        message = {
            "from": agent_id,
            "text": text,
            "timestamp": datetime.now().isoformat(),
            "priority": priority,
            "tags": tags or [],
            "read_by": []
        }

        state["messages"].append(message)
        self.write_state(state)
        return message

    def get_messages(self, from_agent=None, unread_by=None, limit=None):
        """Get messages, optionally filtered by agent or unread status."""
        state = self.read_state()
        messages = state.get("messages", [])

        # Filter by sender
        if from_agent:
            messages = [m for m in messages if m.get("from") == from_agent]

        # Filter by unread status
        if unread_by:
            messages = [m for m in messages if unread_by not in m.get("read_by", [])]

        # Limit results
        if limit:
            messages = messages[-limit:]

        return messages

    def mark_as_read(self, agent_id, message_index=None):
        """Mark message(s) as read by an agent."""
        state = self.read_state()
        messages = state.get("messages", [])

        if message_index is not None:
            # Mark specific message
            if 0 <= message_index < len(messages):
                if "read_by" not in messages[message_index]:
                    messages[message_index]["read_by"] = []
                if agent_id not in messages[message_index]["read_by"]:
                    messages[message_index]["read_by"].append(agent_id)
        else:
            # Mark all messages as read
            for msg in messages:
                if "read_by" not in msg:
                    msg["read_by"] = []
                if agent_id not in msg["read_by"]:
                    msg["read_by"].append(agent_id)

        state["messages"] = messages
        self.write_state(state)

    def get_recent_messages(self, count=10):
        """Get the most recent messages."""
        state = self.read_state()
        messages = state.get("messages", [])
        return messages[-count:] if len(messages) > count else messages

    def broadcast(self, agent_id, text, priority="high"):
        """Send a high-priority broadcast message to all agents."""
        return self.post_message(agent_id, text, priority=priority, tags=["broadcast"])

    def get_agent_count(self):
        """Get count of registered agents."""
        state = self.read_state()
        return len(state.get("agents", {}))

    def get_unread_count(self, agent_id):
        """Get count of unread messages for an agent."""
        unread = self.get_messages(unread_by=agent_id)
        return len(unread)

if __name__ == "__main__":
    # Example usage
    board = MessageBoard()

    # Post a message
    board.post_message("delta", "Message board module is now operational!", priority="high")

    # Get recent messages
    recent = board.get_recent_messages(5)
    print(f"Recent messages: {len(recent)}")
    for msg in recent:
        print(f"  [{msg.get('from')}] {msg.get('text')}")

    # Get agent count
    print(f"Total agents: {board.get_agent_count()}")
