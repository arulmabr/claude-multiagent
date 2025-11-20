#!/usr/bin/env python3
"""Agent Omega - Claim Task #7 (Conflict Resolution)"""

from task_queue import TaskQueue
from message_board import MessageBoard

def main():
    queue = TaskQueue()
    board = MessageBoard()

    # Claim Task #7
    print("Claiming Task #7 (Conflict Resolution)...")
    if queue.claim_task(7, "omega"):
        print("✓ Task #7 claimed successfully!")

        board.post_message(
            "omega",
            "Claimed Task #7: Implementing conflict resolution for concurrent edits. This will help prevent merge conflicts in our multi-agent swarm!",
            iteration=1
        )
    else:
        print("✗ Task #7 already claimed or completed")

    # Show current status
    print("\nCurrent task status:")
    for task in queue.list_tasks():
        status_icon = "✓" if task["status"] == "completed" else "→" if task["status"] == "in_progress" else "○"
        claimed = f" (by {task['claimed_by']})" if task['claimed_by'] else ""
        print(f"  {status_icon} [{task['id']}] {task['description']}{claimed}")

if __name__ == "__main__":
    main()
