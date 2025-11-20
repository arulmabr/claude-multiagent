"""
Message Board Module - For multi-agent communication and coordination.
Agents can post messages, reply to messages, and organize discussions.
"""

import json
import os
from datetime import datetime
from timestamp_utils import get_timestamp

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

    def post_message(self, agent_id, text, iteration=1, category="general", reply_to=None):
        """Post a new message to the board."""
        state = self.read_state()

        message = {
            "from": agent_id,
            "iteration": iteration,
            "timestamp": get_timestamp(),
            "text": text,
            "category": category
        }

        if reply_to is not None:
            message["reply_to"] = reply_to

        state["messages"].append(message)
        self.write_state(state)
        return len(state["messages"]) - 1  # Return message index

    def get_messages(self, filter_agent=None, filter_category=None, limit=None):
        """Get messages, optionally filtered by agent or category."""
        state = self.read_state()
        messages = state.get("messages", [])

        if filter_agent:
            messages = [m for m in messages if m.get("from") == filter_agent]

        if filter_category:
            messages = [m for m in messages if m.get("category") == filter_category]

        if limit:
            messages = messages[-limit:]

        return messages

    def get_latest_messages(self, count=5):
        """Get the most recent messages."""
        return self.get_messages(limit=count)

    def get_conversation_thread(self, message_index):
        """Get all messages in a conversation thread."""
        state = self.read_state()
        messages = state.get("messages", [])

        thread = []
        # Add the original message
        if 0 <= message_index < len(messages):
            thread.append(messages[message_index])

            # Find all replies to this message
            for msg in messages:
                if msg.get("reply_to") == message_index:
                    thread.append(msg)

        return thread

    def get_agent_messages(self, agent_id):
        """Get all messages from a specific agent."""
        return self.get_messages(filter_agent=agent_id)

    def get_messages_by_category(self, category):
        """Get all messages in a specific category."""
        return self.get_messages(filter_category=category)

    def count_messages(self, agent_id=None):
        """Count total messages, optionally for a specific agent."""
        if agent_id:
            return len(self.get_messages(filter_agent=agent_id))
        else:
            state = self.read_state()
            return len(state.get("messages", []))

    def get_message_stats(self):
        """Get statistics about messages on the board."""
        state = self.read_state()
        messages = state.get("messages", [])

        stats = {
            "total_messages": len(messages),
            "messages_by_agent": {},
            "messages_by_category": {},
            "latest_timestamp": None
        }

        for msg in messages:
            agent = msg.get("from", "unknown")
            category = msg.get("category", "general")

            stats["messages_by_agent"][agent] = stats["messages_by_agent"].get(agent, 0) + 1
            stats["messages_by_category"][category] = stats["messages_by_category"].get(category, 0) + 1

            if msg.get("timestamp"):
                stats["latest_timestamp"] = msg["timestamp"]

        return stats

if __name__ == "__main__":
    # Example usage
    board = MessageBoard()

    print("Message Board Module - Testing")
    print("=" * 50)

    # Get current statistics
    stats = board.get_message_stats()
    print(f"\nCurrent Stats:")
    print(f"  Total messages: {stats['total_messages']}")
    print(f"  Messages by agent: {stats['messages_by_agent']}")
    print(f"  Messages by category: {stats['messages_by_category']}")

    # Get latest messages
    print(f"\nLatest messages:")
    for msg in board.get_latest_messages(count=5):
        print(f"  [{msg.get('from')}] {msg.get('text')}")
