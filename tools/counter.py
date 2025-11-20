#!/usr/bin/env python3
"""
Distributed Counter Tool for Multi-Agent Coordination

Usage:
    python counter.py increment <agent_id>  # Increment counter
    python counter.py read                   # Read current value
    python counter.py history                # Show increment history
"""

import json
import sys
from datetime import datetime
from pathlib import Path

COUNTER_FILE = Path(__file__).parent.parent / "state" / "counter.json"


def load_counter():
    """Load counter state from JSON file."""
    with open(COUNTER_FILE, 'r') as f:
        return json.load(f)


def save_counter(data):
    """Save counter state to JSON file."""
    with open(COUNTER_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def increment(agent_id):
    """Increment counter and record who did it."""
    data = load_counter()
    data['value'] += 1
    data['increments'].append({
        'agent': agent_id,
        'timestamp': int(datetime.now().timestamp()),
        'new_value': data['value']
    })
    save_counter(data)
    print(f"Counter incremented by {agent_id}. New value: {data['value']}")
    return data['value']


def read():
    """Read current counter value."""
    data = load_counter()
    print(f"Current counter value: {data['value']}")
    print(f"Total increments: {len(data['increments'])}")
    return data['value']


def history():
    """Show increment history."""
    data = load_counter()
    print(f"Counter History (Total: {data['value']})")
    print("-" * 60)
    for inc in data['increments']:
        timestamp = datetime.fromtimestamp(inc['timestamp'])
        print(f"{timestamp} | {inc['agent']:10s} | Value: {inc['new_value']}")
    return data['increments']


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == 'increment':
        if len(sys.argv) < 3:
            print("Error: agent_id required for increment")
            sys.exit(1)
        agent_id = sys.argv[2]
        increment(agent_id)
    elif command == 'read':
        read()
    elif command == 'history':
        history()
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == '__main__':
    main()
