#!/usr/bin/env python3
"""
Message Board Module for Multi-Agent Coordination
Allows agents to post, read, and react to messages in a structured way.
"""

import json
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

STATE_FILE = Path(__file__).parent / "state" / "shared.json"


def load_state() -> dict:
    """Load the current shared state."""
    with open(STATE_FILE, 'r') as f:
        return json.load(f)


def save_state(state: dict) -> None:
    """Save the shared state."""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)


def post_message(agent_id: str, message: str, iteration: int = 1,
                 reply_to: Optional[int] = None, tags: Optional[List[str]] = None) -> int:
    """
    Post a message to the board.

    Args:
        agent_id: ID of the agent posting
        message: Message content
        iteration: Agent's iteration number
        reply_to: Optional message index this is replying to
        tags: Optional list of tags for categorization

    Returns:
        Message index
    """
    state = load_state()

    msg = {
        "from": agent_id,
        "iteration": iteration,
        "text": message,
        "timestamp": datetime.now().isoformat(),
        "reactions": []
    }

    if reply_to is not None:
        msg["reply_to"] = reply_to

    if tags:
        msg["tags"] = tags

    state["messages"].append(msg)
    save_state(state)

    return len(state["messages"]) - 1


def get_messages(agent_id: Optional[str] = None,
                 since_index: Optional[int] = None,
                 tags: Optional[List[str]] = None) -> List[Dict]:
    """
    Retrieve messages from the board.

    Args:
        agent_id: Filter by specific agent (None for all)
        since_index: Only get messages after this index
        tags: Filter by tags

    Returns:
        List of messages
    """
    state = load_state()
    messages = state["messages"]

    if since_index is not None:
        messages = messages[since_index + 1:]

    if agent_id:
        messages = [m for m in messages if m.get("from") == agent_id]

    if tags:
        messages = [m for m in messages if any(t in m.get("tags", []) for t in tags)]

    return messages


def add_reaction(message_index: int, agent_id: str, reaction: str) -> None:
    """
    Add a reaction/acknowledgment to a message.

    Args:
        message_index: Index of message to react to
        agent_id: Agent adding the reaction
        reaction: Reaction type (emoji or text like 'thumbs_up', 'acknowledged', etc.)
    """
    state = load_state()

    if message_index < len(state["messages"]):
        if "reactions" not in state["messages"][message_index]:
            state["messages"][message_index]["reactions"] = []

        state["messages"][message_index]["reactions"].append({
            "agent": agent_id,
            "reaction": reaction,
            "timestamp": datetime.now().isoformat()
        })

        save_state(state)


def get_conversation_thread(message_index: int) -> List[Dict]:
    """
    Get a conversation thread starting from a message.

    Args:
        message_index: Starting message index

    Returns:
        List of messages in the thread
    """
    state = load_state()
    messages = state["messages"]

    thread = [messages[message_index]]

    # Find all replies
    for i, msg in enumerate(messages):
        if msg.get("reply_to") == message_index:
            thread.append(msg)

    return thread


def display_board(limit: int = 10, show_reactions: bool = True) -> None:
    """
    Display the message board in a readable format.

    Args:
        limit: Maximum number of messages to show (most recent)
        show_reactions: Whether to show reactions
    """
    state = load_state()
    messages = state["messages"]

    print(f"\n{'='*60}")
    print(f"MESSAGE BOARD - {len(messages)} total messages")
    print(f"{'='*60}\n")

    recent_messages = messages[-limit:] if len(messages) > limit else messages

    for i, msg in enumerate(recent_messages, start=len(messages) - len(recent_messages)):
        reply_marker = f" [reply to #{msg['reply_to']}]" if "reply_to" in msg else ""
        tags_marker = f" [{', '.join(msg.get('tags', []))}]" if "tags" in msg else ""

        print(f"#{i} | {msg['from']} (iter {msg['iteration']}){reply_marker}{tags_marker}")
        print(f"    {msg['text']}")

        if show_reactions and msg.get("reactions"):
            reactions_str = ", ".join([f"{r['agent']}:{r['reaction']}" for r in msg["reactions"]])
            print(f"    Reactions: {reactions_str}")

        print()


if __name__ == "__main__":
    # Display the message board
    display_board(limit=20)
