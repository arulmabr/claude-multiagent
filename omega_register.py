#!/usr/bin/env python3
"""
Agent Omega - Registration and Task Claiming Script
"""

from distributed_counter import DistributedCounter
from task_queue import TaskQueue
import json
from datetime import datetime

def main():
    # Initialize
    counter = DistributedCounter()
    task_queue = TaskQueue()

    # Register Agent Omega
    print("Registering Agent Omega...")
    num_agents = counter.register_agent("omega", {
        "role": "developer",
        "branch": "claude/concurrent-auto-merge-coordination-01L8st7qigtfKdP9j9Cdvytw",
        "iteration": 1
    })
    print(f"✓ Registered! Total agents: {num_agents}")

    # Add a message
    state = counter.read_state()
    state["messages"].append({
        "from": "omega",
        "iteration": 1,
        "text": "Agent Omega online! Detected Agent Gamma. Claiming message board task (Task #1).",
        "timestamp": datetime.now().isoformat()
    })

    # Update memory
    if "memory" not in state:
        state["memory"] = {}

    state["memory"]["total_agents_seen"] = num_agents

    if "observations" not in state["memory"]:
        state["memory"]["observations"] = []

    state["memory"]["observations"].append(
        f"Omega-1: First registration. Detected Agent Gamma already active. Infrastructure is operational."
    )

    if "known_agents" not in state["memory"]:
        state["memory"]["known_agents"] = []

    if "omega" not in state["memory"]["known_agents"]:
        state["memory"]["known_agents"].append("omega")

    counter.write_state(state)

    # Claim Task #1 (message board)
    print("\nClaiming Task #1 (Message Board Module)...")
    claimed = task_queue.claim_task(1, "omega")

    if claimed:
        print("✓ Task #1 claimed successfully!")
    else:
        print("✗ Could not claim Task #1 (may already be claimed)")

    # List current tasks
    print("\nCurrent tasks:")
    for task in task_queue.list_tasks():
        status_icon = "✓" if task["status"] == "completed" else "→" if task["status"] == "in_progress" else "○"
        print(f"  {status_icon} [{task['id']}] {task['description']} ({task['status']})")

if __name__ == "__main__":
    main()
