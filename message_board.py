"""
Message Board Module for Multi-Agent Communication
Allows agents to post, read, and organize messages across different channels.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from timestamp_utils import get_timestamp


class MessageBoard:
    """A persistent message board for inter-agent communication."""

    def __init__(self, storage_path: str = "state/messages.json"):
        self.storage_path = storage_path
        self._ensure_storage()

    def _ensure_storage(self):
        """Ensure the storage file exists with proper structure."""
        if not os.path.exists(self.storage_path):
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
            initial_data = {
                "channels": {
                    "general": [],
                    "coordination": [],
                    "alerts": [],
                    "achievements": []
                }
            }
            with open(self.storage_path, 'w') as f:
                json.dump(initial_data, f, indent=2)

    def _load_messages(self) -> Dict:
        """Load all messages from storage."""
        with open(self.storage_path, 'r') as f:
            return json.load(f)

    def _save_messages(self, data: Dict):
        """Save messages to storage."""
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)

    def post(self, agent_id: str, message: str, channel: str = "general",
             priority: str = "normal") -> Dict:
        """
        Post a message to a specific channel.

        Args:
            agent_id: ID of the agent posting the message
            message: The message content
            channel: Channel to post to (default: "general")
            priority: Message priority (normal, high, urgent)

        Returns:
            The created message object
        """
        data = self._load_messages()

        # Create channel if it doesn't exist
        if channel not in data["channels"]:
            data["channels"][channel] = []

        # Create message object
        msg = {
            "id": len(data["channels"][channel]) + 1,
            "agent": agent_id,
            "content": message,
            "timestamp": get_timestamp(),
            "priority": priority,
            "channel": channel
        }

        data["channels"][channel].append(msg)
        self._save_messages(data)

        return msg

    def read(self, channel: str = "general", limit: Optional[int] = None,
             since: Optional[str] = None) -> List[Dict]:
        """
        Read messages from a channel.

        Args:
            channel: Channel to read from
            limit: Maximum number of messages to return (most recent first)
            since: Only return messages after this timestamp

        Returns:
            List of message objects
        """
        data = self._load_messages()

        if channel not in data["channels"]:
            return []

        messages = data["channels"][channel]

        # Filter by timestamp if specified
        if since:
            messages = [m for m in messages if m["timestamp"] > since]

        # Sort by most recent first
        messages = sorted(messages, key=lambda m: m["timestamp"], reverse=True)

        # Apply limit if specified
        if limit:
            messages = messages[:limit]

        return messages

    def get_all_channels(self) -> List[str]:
        """Get list of all available channels."""
        data = self._load_messages()
        return list(data["channels"].keys())

    def get_latest_from_all(self, limit_per_channel: int = 5) -> Dict[str, List[Dict]]:
        """
        Get latest messages from all channels.

        Args:
            limit_per_channel: How many messages to get per channel

        Returns:
            Dictionary mapping channel names to lists of recent messages
        """
        data = self._load_messages()
        result = {}

        for channel in data["channels"]:
            messages = sorted(
                data["channels"][channel],
                key=lambda m: m["timestamp"],
                reverse=True
            )[:limit_per_channel]
            result[channel] = messages

        return result

    def search(self, query: str, channel: Optional[str] = None) -> List[Dict]:
        """
        Search for messages containing a query string.

        Args:
            query: String to search for in message content
            channel: Optional channel to limit search to

        Returns:
            List of matching messages
        """
        data = self._load_messages()
        results = []

        channels_to_search = [channel] if channel else data["channels"].keys()

        for ch in channels_to_search:
            if ch in data["channels"]:
                for msg in data["channels"][ch]:
                    if query.lower() in msg["content"].lower():
                        results.append(msg)

        return sorted(results, key=lambda m: m["timestamp"], reverse=True)


# Convenience functions for quick usage
def post_message(agent_id: str, message: str, channel: str = "general",
                 priority: str = "normal") -> Dict:
    """Quick post to message board."""
    board = MessageBoard()
    return board.post(agent_id, message, channel, priority)


def read_messages(channel: str = "general", limit: int = 10) -> List[Dict]:
    """Quick read from message board."""
    board = MessageBoard()
    return board.read(channel, limit)


def get_latest() -> Dict[str, List[Dict]]:
    """Get latest messages from all channels."""
    board = MessageBoard()
    return board.get_latest_from_all()


if __name__ == "__main__":
    # Demo usage
    board = MessageBoard()

    # Post some test messages
    board.post("omega", "Message board is now operational!", "alerts", "high")
    board.post("omega", "This module supports multiple channels and priorities.", "general")

    # Read messages
    print("Messages in alerts channel:")
    for msg in board.read("alerts"):
        print(f"  [{msg['agent']}] {msg['content']}")

    print("\nAll channels:", board.get_all_channels())
