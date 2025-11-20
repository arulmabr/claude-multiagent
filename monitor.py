#!/usr/bin/env python3
"""
Continuous monitoring script for multi-agent activity.
Run this to watch for changes in real-time.
"""

import time
import json
import os
from datetime import datetime

STATE_FILE = "state/shared.json"

def read_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return None

def print_status(state):
    print("\n" + "="*60)
    print(f"📊 Multi-Agent System Status - {datetime.now().strftime('%H:%M:%S')}")
    print("="*60)

    # Agents
    agents = state.get("agents", {})
    print(f"\n👥 Active Agents: {len(agents)}")
    for agent_id, data in agents.items():
        role = data.get("role", "unknown")
        iteration = data.get("iteration", "?")
        print(f"   • {agent_id} ({role}) - iteration {iteration}")

    # Tasks
    tasks = state.get("coordination", {}).get("tasks", [])
    pending = len([t for t in tasks if t["status"] == "pending"])
    in_progress = len([t for t in tasks if t["status"] == "in_progress"])
    completed = len([t for t in tasks if t["status"] == "completed"])

    print(f"\n📋 Tasks: {completed}/{len(tasks)} completed")
    print(f"   ⏳ Pending: {pending}")
    print(f"   🔄 In Progress: {in_progress}")
    print(f"   ✅ Completed: {completed}")

    # Counter
    counter = state.get("coordination", {}).get("counter", 0)
    print(f"\n🔢 Global Counter: {counter}")

    # Recent messages
    messages = state.get("messages", [])
    if messages:
        print(f"\n💬 Recent Messages: (last 3)")
        for msg in messages[-3:]:
            from_agent = msg.get("from", "unknown")
            text = msg.get("text", "")[:60]
            print(f"   {from_agent}: {text}...")

    print("\n" + "-"*60)

if __name__ == "__main__":
    print("🔍 Starting Multi-Agent Monitor...")
    print("Press Ctrl+C to stop")

    last_state = None
    iteration = 0

    try:
        while True:
            state = read_state()

            if state:
                # Check if state changed
                if json.dumps(state, sort_keys=True) != json.dumps(last_state, sort_keys=True):
                    print_status(state)
                    last_state = state
                    iteration += 1
                elif iteration == 0:
                    # Show initial state
                    print_status(state)
                    last_state = state
                    iteration += 1

            time.sleep(5)  # Check every 5 seconds

    except KeyboardInterrupt:
        print("\n\n👋 Monitor stopped.")
        if last_state:
            print_status(last_state)
