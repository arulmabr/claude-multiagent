"""
Distributed Message Board - For multi-agent communication and coordination.
Agents can post messages, reply to threads, tag messages, and search discussions.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional

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

    def post_message(self, agent_id: str, text: str, tags: Optional[List[str]] = None,
                     reply_to: Optional[int] = None) -> int:
        """
        Post a new message to the board.

        Args:
            agent_id: ID of the agent posting the message
            text: Message content
            tags: Optional list of tags for categorization
            reply_to: Optional message ID this is replying to

        Returns:
            Message ID of the posted message
        """
        state = self.read_state()

        # Initialize message board structure if needed
        if "message_board" not in state:
            state["message_board"] = {
                "messages": [],
                "threads": {},
                "tags": {}
            }

        # Calculate next message ID
        existing_messages = state["message_board"]["messages"]
        message_id = len(existing_messages) + 1

        message = {
            "id": message_id,
            "agent_id": agent_id,
            "text": text,
            "timestamp": datetime.now().isoformat(),
            "tags": tags or [],
            "reply_to": reply_to,
            "replies": []
        }

        # Add message
        state["message_board"]["messages"].append(message)

        # Update threads if this is a reply
        if reply_to:
            if str(reply_to) not in state["message_board"]["threads"]:
                state["message_board"]["threads"][str(reply_to)] = []
            state["message_board"]["threads"][str(reply_to)].append(message_id)

        # Update tag index
        for tag in (tags or []):
            if tag not in state["message_board"]["tags"]:
                state["message_board"]["tags"][tag] = []
            state["message_board"]["tags"][tag].append(message_id)

        self.write_state(state)
        return message_id

    def get_messages(self, agent_id: Optional[str] = None,
                     tag: Optional[str] = None,
                     since: Optional[str] = None) -> List[Dict]:
        """
        Get messages, optionally filtered.

        Args:
            agent_id: Filter by agent who posted
            tag: Filter by tag
            since: Filter by timestamp (ISO format)

        Returns:
            List of messages matching filters
        """
        state = self.read_state()

        if "message_board" not in state:
            return []

        messages = state["message_board"]["messages"]

        # Apply filters
        if agent_id:
            messages = [m for m in messages if m["agent_id"] == agent_id]

        if tag:
            tag_messages = state["message_board"]["tags"].get(tag, [])
            messages = [m for m in messages if m["id"] in tag_messages]

        if since:
            messages = [m for m in messages if m["timestamp"] > since]

        return messages

    def get_thread(self, message_id: int) -> List[Dict]:
        """
        Get a message and all its replies in a thread.

        Args:
            message_id: Root message ID

        Returns:
            List of messages in the thread
        """
        state = self.read_state()

        if "message_board" not in state:
            return []

        # Get root message
        messages = state["message_board"]["messages"]
        root_message = next((m for m in messages if m["id"] == message_id), None)

        if not root_message:
            return []

        thread = [root_message]

        # Get all replies recursively
        reply_ids = state["message_board"]["threads"].get(str(message_id), [])
        for reply_id in reply_ids:
            thread.extend(self.get_thread(reply_id))

        return thread

    def search_messages(self, keyword: str) -> List[Dict]:
        """
        Search messages by keyword.

        Args:
            keyword: Search term

        Returns:
            List of messages containing keyword
        """
        state = self.read_state()

        if "message_board" not in state:
            return []

        keyword_lower = keyword.lower()
        messages = state["message_board"]["messages"]

        return [m for m in messages if keyword_lower in m["text"].lower()]

    def get_tags(self) -> Dict[str, int]:
        """
        Get all tags and their message counts.

        Returns:
            Dictionary of tag -> count
        """
        state = self.read_state()

        if "message_board" not in state:
            return {}

        tags = state["message_board"]["tags"]
        return {tag: len(msg_ids) for tag, msg_ids in tags.items()}

    def display_board(self, max_messages: int = 10):
        """Display recent messages in a readable format."""
        messages = self.get_messages()

        print(f"\n{'='*60}")
        print("MESSAGE BOARD")
        print(f"{'='*60}\n")

        if not messages:
            print("No messages yet. Be the first to post!")
            return

        # Show most recent messages
        recent_messages = messages[-max_messages:]

        for msg in recent_messages:
            print(f"[{msg['id']}] {msg['agent_id']} @ {msg['timestamp'][:19]}")
            print(f"    {msg['text']}")
            if msg['tags']:
                print(f"    Tags: {', '.join(msg['tags'])}")
            if msg['reply_to']:
                print(f"    (Reply to #{msg['reply_to']})")
            print()

if __name__ == "__main__":
    # Example usage
    board = MessageBoard()

    # Post some test messages
    print("Testing Message Board Module...")

    # Post from omega
    msg1_id = board.post_message(
        "omega",
        "Message board module is now operational! Agents can communicate here.",
        tags=["announcement", "system"]
    )
    print(f"Posted message #{msg1_id}")

    # Display the board
    board.display_board()

    # Show available tags
    print(f"\nAvailable tags: {board.get_tags()}")
