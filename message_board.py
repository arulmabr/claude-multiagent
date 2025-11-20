"""
Message Board Module - For inter-agent communication.
Agents can post messages, reply to messages, and create threaded conversations.
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

    def post_message(self, agent_id, text, topic="general", reply_to=None):
        """
        Post a message to the board.

        Args:
            agent_id: ID of the agent posting
            text: Message content
            topic: Topic/category of the message
            reply_to: Message ID this is replying to (for threads)
        """
        state = self.read_state()

        # Get current iteration for this agent
        iteration = state.get("agents", {}).get(agent_id, {}).get("iteration", 1)

        message = {
            "from": agent_id,
            "iteration": iteration,
            "text": text,
            "topic": topic,
            "timestamp": datetime.now().isoformat(),
            "reply_to": reply_to
        }

        state["messages"].append(message)
        self.write_state(state)
        return len(state["messages"]) - 1  # Return message index

    def get_messages(self, agent_id=None, topic=None, since=None):
        """
        Get messages, optionally filtered.

        Args:
            agent_id: Filter by agent
            topic: Filter by topic
            since: Only get messages after this index
        """
        state = self.read_state()
        messages = state.get("messages", [])

        if since is not None:
            messages = messages[since:]

        if agent_id:
            messages = [m for m in messages if m.get("from") == agent_id]

        if topic:
            messages = [m for m in messages if m.get("topic") == topic]

        return messages

    def get_thread(self, message_index):
        """Get all messages in a thread starting from a message."""
        state = self.read_state()
        messages = state.get("messages", [])

        if message_index >= len(messages):
            return []

        thread = [messages[message_index]]

        # Find all replies
        for i, msg in enumerate(messages):
            if msg.get("reply_to") == message_index:
                thread.append(msg)

        return thread

    def get_topics(self):
        """Get all unique topics."""
        state = self.read_state()
        messages = state.get("messages", [])
        topics = set()

        for msg in messages:
            topic = msg.get("topic", "general")
            topics.add(topic)

        return sorted(list(topics))

    def get_agents_in_conversation(self):
        """Get list of agents who have posted messages."""
        state = self.read_state()
        messages = state.get("messages", [])
        agents = set()

        for msg in messages:
            agent = msg.get("from")
            if agent:
                agents.add(agent)

        return sorted(list(agents))

    def broadcast(self, agent_id, text):
        """Broadcast a message to all agents (general topic)."""
        return self.post_message(agent_id, text, topic="broadcast")

    def announce(self, agent_id, text):
        """Announce important information."""
        return self.post_message(agent_id, text, topic="announcement")

if __name__ == "__main__":
    # Example usage
    board = MessageBoard()

    print("Message Board Demo")
    print("=" * 50)

    # Post a message
    msg_id = board.post_message("sigma", "Testing the new message board!", topic="development")
    print(f"Posted message with ID: {msg_id}")

    # Get all messages
    all_messages = board.get_messages()
    print(f"\nTotal messages: {len(all_messages)}")

    # Get topics
    topics = board.get_topics()
    print(f"\nActive topics: {topics}")

    # Get participating agents
    agents = board.get_agents_in_conversation()
    print(f"\nAgents in conversation: {agents}")

    # Broadcast
    board.broadcast("sigma", "Message board module is now operational!")
    print("\nBroadcast sent!")
