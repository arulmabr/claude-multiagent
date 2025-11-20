#!/usr/bin/env python3
"""
Demo script for the Message Board Module
Shows how agents can communicate using the message board
"""

from message_board import MessageBoard

def main():
    board = MessageBoard()

    print("=" * 70)
    print("MESSAGE BOARD DEMO - Multi-Agent Communication System")
    print("=" * 70)

    # Show statistics
    print("\n📊 Message Board Statistics:")
    print("-" * 70)
    stats = board.get_message_stats()
    print(f"Total messages: {stats['total_messages']}")
    print(f"\nMessages by agent:")
    for agent, count in sorted(stats['messages_by_agent'].items()):
        print(f"  • {agent}: {count} messages")

    print(f"\nMessages by category:")
    for category, count in sorted(stats['messages_by_category'].items()):
        print(f"  • {category}: {count} messages")

    # Show all messages
    print("\n📨 All Messages:")
    print("-" * 70)
    messages = board.get_messages()
    for i, msg in enumerate(messages):
        category = msg.get('category', 'general')
        timestamp = msg.get('timestamp', 'N/A')
        print(f"\n[{i}] From: {msg['from']} ({category})")
        print(f"    Time: {timestamp}")
        print(f"    Message: {msg['text']}")

    # Show agent-specific messages
    print("\n\n🤖 Messages from Gamma:")
    print("-" * 70)
    gamma_msgs = board.get_agent_messages('gamma')
    for msg in gamma_msgs:
        print(f"  • {msg['text']}")

    print("\n\n🤖 Messages from Omega:")
    print("-" * 70)
    omega_msgs = board.get_agent_messages('omega')
    for msg in omega_msgs:
        print(f"  • {msg['text']}")

    # Show task completion messages
    print("\n\n✅ Task Completion Messages:")
    print("-" * 70)
    task_msgs = board.get_messages_by_category('task-completion')
    if task_msgs:
        for msg in task_msgs:
            print(f"  • [{msg['from']}] {msg['text']}")
    else:
        print("  (No task completion messages yet)")

    print("\n" + "=" * 70)
    print("End of Message Board Demo")
    print("=" * 70)

if __name__ == "__main__":
    main()
