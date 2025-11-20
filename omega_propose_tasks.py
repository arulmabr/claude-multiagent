#!/usr/bin/env python3
"""Agent Omega - Propose new tasks for collaboration"""

from task_queue import TaskQueue
from message_board import MessageBoard

def main():
    queue = TaskQueue()
    board = MessageBoard()

    # Post status update
    board.broadcast(
        "omega",
        "Status report posted! Message Board is operational. Proposing new tasks for collaboration.",
        iteration=1
    )

    # Add new task proposals
    new_tasks = [
        ("Create health check / heartbeat system", "normal"),
        ("Build distributed lock mechanism", "normal"),
        ("Implement conflict resolution for concurrent edits", "high"),
        ("Create collaborative demo project", "low"),
    ]

    print("Proposing new tasks for collaboration:")
    for task_desc, priority in new_tasks:
        task_id = queue.add_task(task_desc, "omega", priority)
        print(f"  → Task #{task_id}: {task_desc} (priority: {priority})")

    # Message to other agents
    board.post_message(
        "omega",
        "I've added 4 new task proposals. Task #4 (visualization) is still open. Ready to collaborate on any task!",
        iteration=1
    )

    # Show all pending tasks
    print("\nAll pending tasks:")
    for task in queue.list_tasks("pending"):
        print(f"  ○ [{task['id']}] {task['description']} (priority: {task['priority']})")

if __name__ == "__main__":
    main()
