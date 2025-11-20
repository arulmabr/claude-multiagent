"""
Message Board Module for Multi-Agent Coordination

Provides a structured way for agents to post and read messages.
Supports categories, priority levels, and message threading.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


STATE_FILE = Path(__file__).parent / "state" / "shared.json"


def load_state() -> Dict:
    """Load the shared state file."""
    with open(STATE_FILE, 'r') as f:
        return json.load(f)


def save_state(state: Dict) -> None:
    """Save the shared state file."""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)


def post_message(
    agent_id: str,
    text: str,
    category: str = "general",
    priority: str = "normal",
    reply_to: Optional[int] = None,
    iteration: Optional[int] = None
) -> int:
    """
    Post a message to the board.

    Args:
        agent_id: ID of the agent posting the message
        text: Message content
        category: Category (general, task, coordination, debug, celebration)
        priority: Priority level (low, normal, high, urgent)
        reply_to: Optional message ID this is replying to
        iteration: Optional iteration number

    Returns:
        Message ID of the posted message
    """
    state = load_state()

    # Find the next message ID
    messages = state.get("messages", [])
    if messages:
        # Look for messages with IDs
        max_id = max([m.get("id", 0) for m in messages])
        message_id = max_id + 1
    else:
        message_id = 1

    message = {
        "id": message_id,
        "from": agent_id,
        "text": text,
        "category": category,
        "priority": priority,
        "timestamp": datetime.utcnow().isoformat(),
        "iteration": iteration
    }

    if reply_to is not None:
        message["reply_to"] = reply_to

    messages.append(message)
    state["messages"] = messages

    save_state(state)
    return message_id


def get_messages(
    category: Optional[str] = None,
    agent_id: Optional[str] = None,
    min_priority: Optional[str] = None,
    since_id: Optional[int] = None
) -> List[Dict]:
    """
    Retrieve messages with optional filtering.

    Args:
        category: Filter by category
        agent_id: Filter by agent ID
        min_priority: Minimum priority level
        since_id: Only messages after this ID

    Returns:
        List of matching messages
    """
    state = load_state()
    messages = state.get("messages", [])

    priority_levels = {"low": 0, "normal": 1, "high": 2, "urgent": 3}
    min_priority_level = priority_levels.get(min_priority, -1) if min_priority else -1

    filtered = []
    for msg in messages:
        # Apply filters
        if category and msg.get("category") != category:
            continue
        if agent_id and msg.get("from") != agent_id:
            continue
        if since_id and msg.get("id", 0) <= since_id:
            continue
        if min_priority:
            msg_priority = priority_levels.get(msg.get("priority", "normal"), 1)
            if msg_priority < min_priority_level:
                continue

        filtered.append(msg)

    return filtered


def get_thread(message_id: int) -> List[Dict]:
    """
    Get a message and all its replies.

    Args:
        message_id: ID of the original message

    Returns:
        List of messages in the thread, ordered chronologically
    """
    state = load_state()
    messages = state.get("messages", [])

    # Find the original message
    original = None
    for msg in messages:
        if msg.get("id") == message_id:
            original = msg
            break

    if not original:
        return []

    # Find all replies
    thread = [original]
    for msg in messages:
        if msg.get("reply_to") == message_id:
            thread.append(msg)

    return thread


def get_unread_messages(agent_id: str, last_read_id: int = 0) -> List[Dict]:
    """
    Get messages posted since the agent last checked.

    Args:
        agent_id: ID of the agent checking messages
        last_read_id: ID of the last message the agent read

    Returns:
        List of new messages
    """
    messages = get_messages(since_id=last_read_id)
    # Exclude messages from the agent itself
    return [m for m in messages if m.get("from") != agent_id]


def get_message_stats() -> Dict:
    """
    Get statistics about messages on the board.

    Returns:
        Dictionary with message statistics
    """
    state = load_state()
    messages = state.get("messages", [])

    stats = {
        "total_messages": len(messages),
        "by_agent": {},
        "by_category": {},
        "by_priority": {}
    }

    for msg in messages:
        agent = msg.get("from", "unknown")
        category = msg.get("category", "general")
        priority = msg.get("priority", "normal")

        stats["by_agent"][agent] = stats["by_agent"].get(agent, 0) + 1
        stats["by_category"][category] = stats["by_category"].get(category, 0) + 1
        stats["by_priority"][priority] = stats["by_priority"].get(priority, 0) + 1

    return stats


if __name__ == "__main__":
    # Example usage
    print("Message Board Module")
    print("=" * 50)

    stats = get_message_stats()
    print(f"\nTotal messages: {stats['total_messages']}")
    print(f"By agent: {stats['by_agent']}")
    print(f"By category: {stats['by_category']}")
    print(f"By priority: {stats['by_priority']}")

    print("\nRecent messages:")
    recent = get_messages()[-5:]  # Last 5 messages
    for msg in recent:
        print(f"  [{msg.get('from')}] {msg.get('text')[:60]}...")
