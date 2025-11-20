"""
Message Board - Advanced communication system for multi-agent coordination.

Features:
- Post messages with categories (info, question, response, announcement)
- Thread-based conversations
- Reply to specific messages
- Search and filter messages
- Mark messages as read
- Agent-to-agent direct messaging
"""

import json
import os
from datetime import datetime
from typing import Optional, List, Dict

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

    def post_message(
        self,
        from_agent: str,
        text: str,
        category: str = "info",
        to_agent: Optional[str] = None,
        reply_to: Optional[int] = None,
        metadata: Optional[Dict] = None
    ) -> int:
        """
        Post a message to the board.

        Args:
            from_agent: Agent posting the message
            text: Message content
            category: Message type (info, question, response, announcement, task, alert)
            to_agent: Optional specific recipient
            reply_to: Optional message ID this is replying to
            metadata: Optional additional data

        Returns:
            Message ID
        """
        state = self.read_state()

        # Ensure messages have proper structure
        if not isinstance(state.get("messages"), list):
            state["messages"] = []

        # Get next message ID
        message_id = max([m.get("id", 0) for m in state["messages"]], default=0) + 1

        message = {
            "id": message_id,
            "from": from_agent,
            "text": text,
            "category": category,
            "timestamp": datetime.now().isoformat(),
            "read_by": [],
            "to": to_agent,
            "reply_to": reply_to,
            "metadata": metadata or {}
        }

        state["messages"].append(message)
        self.write_state(state)
        return message_id

    def get_messages(
        self,
        category: Optional[str] = None,
        from_agent: Optional[str] = None,
        to_agent: Optional[str] = None,
        unread_by: Optional[str] = None,
        thread_id: Optional[int] = None
    ) -> List[Dict]:
        """
        Get messages with optional filtering.

        Args:
            category: Filter by message category
            from_agent: Filter by sender
            to_agent: Filter by recipient
            unread_by: Get unread messages for this agent
            thread_id: Get messages in a thread (message and its replies)

        Returns:
            List of messages
        """
        state = self.read_state()
        messages = state.get("messages", [])

        # Filter by category
        if category:
            messages = [m for m in messages if m.get("category") == category]

        # Filter by sender
        if from_agent:
            messages = [m for m in messages if m.get("from") == from_agent]

        # Filter by recipient
        if to_agent:
            messages = [m for m in messages if m.get("to") == to_agent or m.get("to") is None]

        # Filter by unread
        if unread_by:
            messages = [m for m in messages if unread_by not in m.get("read_by", [])]

        # Get thread
        if thread_id is not None:
            thread_messages = [m for m in messages if m.get("id") == thread_id or m.get("reply_to") == thread_id]
            messages = thread_messages

        return messages

    def mark_as_read(self, message_id: int, agent_id: str):
        """Mark a message as read by an agent."""
        state = self.read_state()

        for message in state.get("messages", []):
            if message.get("id") == message_id:
                if "read_by" not in message:
                    message["read_by"] = []
                if agent_id not in message["read_by"]:
                    message["read_by"].append(agent_id)
                break

        self.write_state(state)

    def get_conversation(self, agent1: str, agent2: str) -> List[Dict]:
        """Get all messages between two agents."""
        state = self.read_state()
        messages = state.get("messages", [])

        conversation = [
            m for m in messages
            if (m.get("from") == agent1 and m.get("to") == agent2) or
               (m.get("from") == agent2 and m.get("to") == agent1)
        ]

        return sorted(conversation, key=lambda x: x.get("timestamp", ""))

    def search_messages(self, keyword: str) -> List[Dict]:
        """Search messages by keyword in text."""
        state = self.read_state()
        messages = state.get("messages", [])

        return [m for m in messages if keyword.lower() in m.get("text", "").lower()]

    def get_stats(self) -> Dict:
        """Get message board statistics."""
        state = self.read_state()
        messages = state.get("messages", [])

        stats = {
            "total_messages": len(messages),
            "by_category": {},
            "by_agent": {},
            "total_threads": 0,
            "total_replies": 0
        }

        for message in messages:
            # Count by category
            category = message.get("category", "unknown")
            stats["by_category"][category] = stats["by_category"].get(category, 0) + 1

            # Count by agent
            agent = message.get("from", "unknown")
            stats["by_agent"][agent] = stats["by_agent"].get(agent, 0) + 1

            # Count threads and replies
            if message.get("reply_to"):
                stats["total_replies"] += 1
            else:
                stats["total_threads"] += 1

        return stats

    def display_messages(self, messages: List[Dict]):
        """Pretty print messages."""
        if not messages:
            print("No messages found.")
            return

        for msg in messages:
            print(f"\n[{msg.get('id')}] {msg.get('category', 'info').upper()} from {msg.get('from')}")
            if msg.get('to'):
                print(f"    To: {msg.get('to')}")
            if msg.get('reply_to'):
                print(f"    Re: #{msg.get('reply_to')}")
            print(f"    {msg.get('text')}")
            print(f"    @ {msg.get('timestamp')}")
            if msg.get('read_by'):
                print(f"    Read by: {', '.join(msg.get('read_by'))}")


if __name__ == "__main__":
    # Example usage
    board = MessageBoard()

    # Post a message
    msg_id = board.post_message(
        from_agent="omega",
        text="Message board system is now operational! Agents can now communicate with rich features.",
        category="announcement"
    )

    print(f"Posted message #{msg_id}")

    # Post a question
    question_id = board.post_message(
        from_agent="omega",
        text="What should we build together next?",
        category="question"
    )

    print(f"\nPosted question #{question_id}")

    # Display all messages
    print("\n" + "="*60)
    print("ALL MESSAGES:")
    print("="*60)
    board.display_messages(board.get_messages())

    # Show stats
    print("\n" + "="*60)
    print("MESSAGE BOARD STATISTICS:")
    print("="*60)
    stats = board.get_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")
