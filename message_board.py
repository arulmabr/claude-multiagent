"""
Message Board - A communication system for multi-agent coordination.
Agents can post messages, read messages, and filter by agent or iteration.
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

    def post_message(self, agent_id, text, iteration=None, metadata=None):
        """Post a message to the board."""
        state = self.read_state()

        if "messages" not in state:
            state["messages"] = []

        message = {
            "from": agent_id,
            "text": text,
            "timestamp": datetime.now().isoformat(),
        }

        if iteration is not None:
            message["iteration"] = iteration

        if metadata:
            message.update(metadata)

        state["messages"].append(message)
        self.write_state(state)
        return len(state["messages"])

    def get_messages(self, agent_id=None, iteration=None, limit=None):
        """Get messages, optionally filtered by agent or iteration."""
        state = self.read_state()
        messages = state.get("messages", [])

        # Filter by agent
        if agent_id:
            messages = [m for m in messages if m.get("from") == agent_id]

        # Filter by iteration
        if iteration is not None:
            messages = [m for m in messages if m.get("iteration") == iteration]

        # Apply limit
        if limit:
            messages = messages[-limit:]

        return messages

    def get_latest_message(self, agent_id=None):
        """Get the most recent message, optionally from a specific agent."""
        messages = self.get_messages(agent_id=agent_id, limit=1)
        return messages[0] if messages else None

    def get_all_messages(self):
        """Get all messages in chronological order."""
        return self.get_messages()

    def count_messages(self, agent_id=None):
        """Count total messages, optionally for a specific agent."""
        return len(self.get_messages(agent_id=agent_id))

    def broadcast(self, agent_id, text, iteration=None):
        """Broadcast a message to all agents."""
        return self.post_message(
            agent_id,
            text,
            iteration=iteration,
            metadata={"type": "broadcast"}
        )

    def reply_to(self, agent_id, text, reply_to_agent, iteration=None):
        """Post a message as a reply to another agent."""
        return self.post_message(
            agent_id,
            text,
            iteration=iteration,
            metadata={"type": "reply", "reply_to": reply_to_agent}
        )

    def clear_old_messages(self, keep_last_n=50):
        """Keep only the most recent N messages to prevent unbounded growth."""
        state = self.read_state()

        if "messages" in state and len(state["messages"]) > keep_last_n:
            state["messages"] = state["messages"][-keep_last_n:]
            self.write_state(state)
            return True

        return False

if __name__ == "__main__":
    # Example usage
    board = MessageBoard()

    # Post a message
    board.post_message("omega", "Message Board module is now operational!", iteration=1)

    # Broadcast
    board.broadcast("omega", "All agents: Message Board is ready for use!")

    # Get all messages
    print("All messages:")
    for msg in board.get_all_messages():
        agent = msg.get("from", "unknown")
        text = msg.get("text", "")
        iteration = msg.get("iteration", "?")
        print(f"  [{agent}:{iteration}] {text}")

    print(f"\nTotal messages: {board.count_messages()}")
