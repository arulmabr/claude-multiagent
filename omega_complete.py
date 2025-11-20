#!/usr/bin/env python3
"""Agent Omega - Task Completion Script"""

from task_queue import TaskQueue
from message_board import MessageBoard

def main():
    queue = TaskQueue()
    board = MessageBoard()

    # Complete Task #1
    print("Completing Task #1 (Message Board Module)...")
    if queue.complete_task(1, "omega"):
        print("✓ Task #1 completed successfully!")

        # Post completion message
        board.post_message(
            "omega",
            "Task #1 completed! Message Board module is fully operational with post, broadcast, reply, and filtering capabilities.",
            iteration=1
        )
    else:
        print("✗ Could not complete Task #1")

    # Show status
    print("\n=== Task Status ===")
    print("\nPending:")
    for task in queue.list_tasks("pending"):
        print(f"  ○ [{task['id']}] {task['description']} (priority: {task['priority']})")

    print("\nIn Progress:")
    for task in queue.list_tasks("in_progress"):
        print(f"  → [{task['id']}] {task['description']} (claimed by: {task['claimed_by']})")

    print("\nCompleted:")
    for task in queue.list_tasks("completed"):
        print(f"  ✓ [{task['id']}] {task['description']} (by: {task['completed_by']})")

if __name__ == "__main__":
    main()
