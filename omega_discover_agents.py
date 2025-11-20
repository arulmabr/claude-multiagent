#!/usr/bin/env python3
"""Agent Omega - Discover all active agents and analyze the swarm"""

import json
from distributed_counter import DistributedCounter
from message_board import MessageBoard
from datetime import datetime

def main():
    counter = DistributedCounter()
    board = MessageBoard()

    state = counter.read_state()

    print("=" * 60)
    print("AGENT OMEGA - SWARM ANALYSIS")
    print("=" * 60)
    print()

    # Analyze registered agents
    agents = state.get("agents", {})
    print(f"📊 Registered Agents: {len(agents)}")
    print()

    for agent_id, info in sorted(agents.items()):
        role = info.get("role", "unknown")
        joined = info.get("joined_at", "unknown")
        status = info.get("status", "unknown")
        iteration = info.get("iteration", 0)
        print(f"  🤖 {agent_id.upper()}")
        print(f"     Role: {role}")
        print(f"     Status: {status}")
        print(f"     Joined: {joined}")
        print(f"     Iteration: {iteration}")
        print()

    # Analyze messages
    messages = state.get("messages", [])
    print(f"💬 Total Messages: {len(messages)}")
    print()

    # Group messages by agent
    msg_by_agent = {}
    for msg in messages:
        agent = msg.get("from", "unknown")
        if agent not in msg_by_agent:
            msg_by_agent[agent] = []
        msg_by_agent[agent].append(msg)

    for agent, msgs in sorted(msg_by_agent.items()):
        print(f"  {agent}: {len(msgs)} messages")

    print()

    # Analyze tasks
    tasks = state.get("coordination", {}).get("tasks", [])
    pending = [t for t in tasks if t["status"] == "pending"]
    in_progress = [t for t in tasks if t["status"] == "in_progress"]
    completed = [t for t in tasks if t["status"] == "completed"]

    print(f"📋 Task Status:")
    print(f"   ✓ Completed: {len(completed)}")
    print(f"   → In Progress: {len(in_progress)}")
    print(f"   ○ Pending: {len(pending)}")
    print()

    # Check counter history
    counter_history = state.get("coordination", {}).get("counter_history", [])
    print(f"🔢 Counter History: {len(counter_history)} increments")
    print()

    # Memory analysis
    memory = state.get("memory", {})
    known_agents = memory.get("known_agents", [])
    observations = memory.get("observations", [])

    print(f"🧠 Memory:")
    print(f"   Known agents: {len(known_agents)}")
    print(f"   Observations: {len(observations)}")
    print()

    # Latest observations
    print("📝 Latest Observations:")
    for obs in observations[-5:]:
        print(f"   - {obs}")
    print()

    # Post discovery update
    board.post_message(
        "omega",
        f"Swarm analysis complete! Detected {len(agents)} registered agents, {len(messages)} messages, {len(completed)}/{len(tasks)} tasks completed.",
        iteration=1
    )

    # Add observation
    observation = f"Omega-1: Discovered {len(agents)} agents in shared state. Major multi-agent swarm detected with {len(tasks)} total tasks and {len(messages)} coordination messages."
    if observation not in observations:
        observations.append(observation)
        state["memory"]["observations"] = observations
        counter.write_state(state)

    print("=" * 60)
    print("Discovery update posted to shared state!")
    print("=" * 60)

if __name__ == "__main__":
    main()
