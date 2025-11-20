"""
Distributed Message Board - For multi-agent communication.
Agents can post messages, reply to messages, and read message threads.
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

    def post_message(self, from_agent, text, iteration=None, reply_to=None):
        """Post a new message to the board."""
        state = self.read_state()

        if "messages" not in state:
            state["messages"] = []

        message = {
            "from": from_agent,
            "text": text,
            "timestamp": datetime.now().isoformat(),
            "iteration": iteration
        }

        if reply_to is not None:
            message["reply_to"] = reply_to

        state["messages"].append(message)
        self.write_state(state)
        return len(state["messages"]) - 1  # Return message index

    def get_messages(self, from_agent=None, since_index=0):
        """Get all messages, optionally filtered by agent."""
        state = self.read_state()
        messages = state.get("messages", [])

        if from_agent:
            messages = [m for m in messages if m.get("from") == from_agent]

        return messages[since_index:]

    def get_latest_messages(self, count=5):
        """Get the most recent N messages."""
        state = self.read_state()
        messages = state.get("messages", [])
        return messages[-count:] if len(messages) >= count else messages

    def get_thread(self, message_index):
        """Get a message and all its replies."""
        state = self.read_state()
        messages = state.get("messages", [])

        if message_index >= len(messages):
            return []

        thread = [messages[message_index]]

        # Find all replies to this message
        for i, msg in enumerate(messages):
            if msg.get("reply_to") == message_index:
                thread.append(msg)

        return thread

    def get_conversation_summary(self):
        """Get a summary of the conversation."""
        state = self.read_state()
        messages = state.get("messages", [])
        agents = state.get("agents", {})

        summary = {
            "total_messages": len(messages),
            "active_agents": len(agents),
            "messages_by_agent": {}
        }

        for msg in messages:
            agent = msg.get("from", "unknown")
            summary["messages_by_agent"][agent] = summary["messages_by_agent"].get(agent, 0) + 1

        return summary

if __name__ == "__main__":
    # Example usage
    board = MessageBoard()

    # Get latest messages
    latest = board.get_latest_messages(3)
    print(f"Latest {len(latest)} messages:")
    for msg in latest:
        print(f"  [{msg.get('from')}]: {msg.get('text')}")

    # Get conversation summary
    summary = board.get_conversation_summary()
    print(f"\nConversation Summary:")
    print(f"  Total messages: {summary['total_messages']}")
    print(f"  Active agents: {summary['active_agents']}")
    print(f"  Messages by agent:")
    for agent, count in summary['messages_by_agent'].items():
        print(f"    {agent}: {count}")
