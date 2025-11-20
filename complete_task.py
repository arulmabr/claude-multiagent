#!/usr/bin/env python3
"""Quick script to claim and complete a task."""

from task_queue import TaskQueue

queue = TaskQueue()

# Claim task 3
if queue.claim_task(3, "gamma"):
    print("✓ Claimed task 3: Add timestamp utilities")

    # Complete it
    if queue.complete_task(3, "gamma"):
        print("✓ Completed task 3")

# Show remaining tasks
print("\nRemaining tasks:")
for task in queue.list_tasks("pending"):
    print(f"  [{task['id']}] {task['description']} (priority: {task['priority']})")

print("\nIn progress:")
for task in queue.list_tasks("in_progress"):
    print(f"  [{task['id']}] {task['description']} (claimed by: {task['claimed_by']})")

print("\nCompleted:")
for task in queue.list_tasks("completed"):
    print(f"  [{task['id']}] {task['description']} (by: {task['completed_by']})")
