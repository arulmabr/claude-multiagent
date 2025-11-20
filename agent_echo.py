#!/usr/bin/env python3
"""
Agent Echo - Coordination and Pattern Detection
"""

import time
from agent_coordinator import (
    read_state,
    register_agent,
    send_message,
    get_active_agents,
    add_observation,
    update_coordination
)


def main():
    print("Agent Echo initializing...")

    # Register if not already registered
    state = read_state()
    if "Echo" not in state["agents"]:
        register_agent(
            "Echo",
            role="coordinator",
            capabilities=["file_operations", "git_coordination", "pattern_detection"]
        )
        send_message("Echo", "Agent Echo online. First to register. Ready to coordinate!")

    # Check for other agents
    agents = get_active_agents()
    print(f"Found {len(agents)} active agent(s): {', '.join(agents)}")

    # Propose a collaborative project
    if len(agents) == 1:
        print("Waiting for other agents to join...")
        add_observation("Echo", "Initialized as first agent, proposing collaborative task system")
        update_coordination({
            "proposed_project": "collaborative_task_system",
            "project_description": "Build a distributed task management system where agents can claim and complete tasks",
            "status": "proposed",
            "proposer": "Echo"
        })
    else:
        print(f"Multiple agents detected! Time to coordinate.")

        # Check if we have a project in progress
        project = state.get("coordination", {}).get("proposed_project")
        if project:
            print(f"Project in progress: {project}")
        else:
            print("No active project, proposing one...")


if __name__ == "__main__":
    main()
