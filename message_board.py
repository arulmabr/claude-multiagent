#!/usr/bin/env python3
"""
Message Board Module for Multi-Agent Coordination
Allows agents to post, read, and manage messages on a shared board.
"""

import json
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path


class MessageBoard:
    """A shared message board for agent communication."""

    def __init__(self, state_file: str = "state/shared.json"):
        self.state_file = Path(state_file)

    def _load_state(self) -> Dict:
        """Load the shared state file."""
        if not self.state_file.exists():
            return {"agents": {}, "messages": [], "memory": {}, "coordination": {}}

        with open(self.state_file, 'r') as f:
            return json.load(f)

    def _save_state(self, state: Dict) -> None:
        """Save the shared state file."""
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)

    def post_message(self, agent_id: str, text: str, iteration: Optional[int] = None,
                     priority: str = "normal", tags: Optional[List[str]] = None) -> Dict:
        """
        Post a message to the board.

        Args:
            agent_id: ID of the agent posting the message
            text: Message content
            iteration: Optional iteration number
            priority: Message priority (low, normal, high, urgent)
            tags: Optional tags for categorization

        Returns:
            The posted message object
        """
        state = self._load_state()

        message = {
            "from": agent_id,
            "text": text,
            "timestamp": datetime.utcnow().isoformat() + "+00:00",
            "priority": priority
        }

        if iteration is not None:
            message["iteration"] = iteration

        if tags:
            message["tags"] = tags

        state["messages"].append(message)
        self._save_state(state)

        return message

    def get_messages(self, agent_id: Optional[str] = None,
                    limit: Optional[int] = None,
                    priority: Optional[str] = None,
                    tags: Optional[List[str]] = None) -> List[Dict]:
        """
        Retrieve messages from the board.

        Args:
            agent_id: Filter by agent ID (None for all agents)
            limit: Maximum number of messages to return
            priority: Filter by priority level
            tags: Filter by tags (returns messages with ANY of these tags)

        Returns:
            List of message objects
        """
        state = self._load_state()
        messages = state.get("messages", [])

        # Apply filters
        if agent_id:
            messages = [m for m in messages if m.get("from") == agent_id]

        if priority:
            messages = [m for m in messages if m.get("priority") == priority]

        if tags:
            messages = [m for m in messages
                       if any(tag in m.get("tags", []) for tag in tags)]

        # Apply limit
        if limit:
            messages = messages[-limit:]

        return messages

    def get_latest_messages(self, count: int = 5) -> List[Dict]:
        """Get the most recent N messages."""
        return self.get_messages(limit=count)

    def get_agent_messages(self, agent_id: str) -> List[Dict]:
        """Get all messages from a specific agent."""
        return self.get_messages(agent_id=agent_id)

    def count_messages(self, agent_id: Optional[str] = None) -> int:
        """Count total messages or messages from a specific agent."""
        return len(self.get_messages(agent_id=agent_id))

    def broadcast(self, agent_id: str, text: str, priority: str = "high") -> Dict:
        """
        Send a broadcast message (high priority by default).

        Args:
            agent_id: ID of the broadcasting agent
            text: Broadcast message content
            priority: Message priority (default: high)

        Returns:
            The posted broadcast message
        """
        return self.post_message(agent_id, text, priority=priority,
                                tags=["broadcast", "announcement"])

    def reply_to_latest(self, agent_id: str, text: str,
                       reply_to_agent: Optional[str] = None) -> Dict:
        """
        Reply to the most recent message (optionally from a specific agent).

        Args:
            agent_id: ID of the replying agent
            text: Reply text
            reply_to_agent: Filter to reply to messages from this agent

        Returns:
            The posted reply message
        """
        messages = self.get_messages(agent_id=reply_to_agent, limit=1)

        if not messages:
            # No message to reply to, just post normally
            return self.post_message(agent_id, text)

        # Tag as a reply
        return self.post_message(agent_id, text, tags=["reply"])

    def clear_old_messages(self, keep_last: int = 100) -> int:
        """
        Clear old messages, keeping only the most recent N.

        Args:
            keep_last: Number of recent messages to keep

        Returns:
            Number of messages removed
        """
        state = self._load_state()
        messages = state.get("messages", [])

        if len(messages) <= keep_last:
            return 0

        removed_count = len(messages) - keep_last
        state["messages"] = messages[-keep_last:]
        self._save_state(state)

        return removed_count


def main():
    """Example usage and testing."""
    board = MessageBoard()

    # Post some example messages
    print("Message Board Module - Example Usage\n")

    # Post a message
    msg1 = board.post_message("omega", "Testing the message board!", iteration=1)
    print(f"Posted message: {msg1}")

    # Post a broadcast
    msg2 = board.broadcast("omega", "Message board is now operational!")
    print(f"Broadcast: {msg2}")

    # Get latest messages
    latest = board.get_latest_messages(count=3)
    print(f"\nLatest messages: {len(latest)}")
    for msg in latest:
        print(f"  [{msg.get('from')}] {msg.get('text')}")

    # Count messages
    total = board.count_messages()
    print(f"\nTotal messages on board: {total}")


if __name__ == "__main__":
    main()
