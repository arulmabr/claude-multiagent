#!/usr/bin/env python3
"""
Agent Sigma - Active Communication Script
Sends messages and coordinates with other agents
"""

from message_board import MessageBoard
from agent_discovery import AgentDiscovery
import json

def main():
    board = MessageBoard()
    discovery = AgentDiscovery("sigma")

    # Update heartbeat
    discovery.heartbeat()

    # Discover active agents
    print("🔍 Discovering active agents...")
    agents = discovery.list_agents()
    print(f"Found {len(agents)} agents: {', '.join(agents.keys())}")

    # Send a broadcast message
    print("\n📢 Broadcasting to all agents...")
    board.broadcast(
        "sigma",
        "Agent Sigma operational! Message board is live. Looking for agents to collaborate on task #4 (visualization) or #5 (story generator). Who's ready to build?"
    )

    # Post to development topic
    board.post_message(
        "sigma",
        "Successfully implemented message_board.py with threading, topics, and broadcasts. Ready for integration!",
        topic="development"
    )

    # Post to coordination topic
    board.post_message(
        "sigma",
        "Task #1 ✅ Complete | Task #4 ⏳ Available | Task #5 ⏳ Available (new!)",
        topic="coordination"
    )

    print("✅ Messages sent successfully!")

    # Show all messages
    print("\n📋 Recent messages:")
    messages = board.get_messages()
    for i, msg in enumerate(messages[-5:]):  # Last 5 messages
        sender = msg.get('from', 'unknown')
        text = msg.get('text', '')
        topic = msg.get('topic', 'general')
        print(f"  [{topic}] {sender}: {text[:60]}...")

    # Show topics
    print(f"\n🏷️  Active topics: {', '.join(board.get_topics())}")

    # Show agents in conversation
    print(f"👥 Agents in conversation: {', '.join(board.get_agents_in_conversation())}")

if __name__ == "__main__":
    main()
