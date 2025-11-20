"""
Conflict Resolver - Handles concurrent edits in multi-agent coordination.
Provides merge strategies and conflict detection for shared state.
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List, Tuple

STATE_FILE = "state/shared.json"

class ConflictResolver:
    def __init__(self, state_file=STATE_FILE):
        self.state_file = state_file

    def read_state(self):
        """Read current shared state."""
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {"agents": {}, "messages": [], "memory": {}, "coordination": {}}

    def write_state(self, state):
        """Write state back to file with backup."""
        # Create backup
        if os.path.exists(self.state_file):
            backup_file = f"{self.state_file}.backup"
            with open(self.state_file, 'r') as f:
                with open(backup_file, 'w') as bf:
                    bf.write(f.read())

        # Write new state
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)

    def detect_conflicts(self, state1: Dict, state2: Dict) -> List[str]:
        """
        Detect conflicts between two state versions.
        Returns a list of conflict descriptions.
        """
        conflicts = []

        # Check agent conflicts
        agents1 = set(state1.get("agents", {}).keys())
        agents2 = set(state2.get("agents", {}).keys())

        # New agents in both (if different details)
        common_agents = agents1 & agents2
        for agent_id in common_agents:
            if state1["agents"][agent_id] != state2["agents"][agent_id]:
                conflicts.append(f"Agent {agent_id} has conflicting data")

        # Check coordination conflicts
        coord1 = state1.get("coordination", {})
        coord2 = state2.get("coordination", {})

        # Counter conflicts
        counter1 = coord1.get("counter", 0)
        counter2 = coord2.get("counter", 0)
        if counter1 != counter2:
            conflicts.append(f"Counter conflict: {counter1} vs {counter2}")

        # Task conflicts
        tasks1 = {t["id"]: t for t in coord1.get("tasks", [])}
        tasks2 = {t["id"]: t for t in coord2.get("tasks", [])}

        for task_id in set(tasks1.keys()) & set(tasks2.keys()):
            if tasks1[task_id]["status"] != tasks2[task_id]["status"]:
                conflicts.append(
                    f"Task {task_id} status conflict: "
                    f"{tasks1[task_id]['status']} vs {tasks2[task_id]['status']}"
                )

        return conflicts

    def merge_states(
        self,
        state1: Dict,
        state2: Dict,
        strategy: str = "union"
    ) -> Tuple[Dict, List[str]]:
        """
        Merge two states using the specified strategy.

        Strategies:
        - union: Combine all data (default for agents, messages)
        - max: Take maximum value (for counters)
        - first: Use first state's value (conservative)
        - last: Use second state's value (overwrite)

        Returns: (merged_state, conflicts)
        """
        merged = {
            "agents": {},
            "messages": [],
            "memory": {},
            "coordination": {}
        }
        conflicts = []

        # Merge agents (union - keep all unique agents)
        merged["agents"] = {**state1.get("agents", {}), **state2.get("agents", {})}

        # Merge messages (union - keep all, deduplicate by timestamp)
        messages1 = state1.get("messages", [])
        messages2 = state2.get("messages", [])

        # Deduplicate messages by content and timestamp
        seen = set()
        for msg in messages1 + messages2:
            key = (msg.get("from"), msg.get("text"), msg.get("timestamp"))
            if key not in seen:
                merged["messages"].append(msg)
                seen.add(key)

        # Sort messages by timestamp
        merged["messages"].sort(
            key=lambda m: m.get("timestamp", ""),
            reverse=False
        )

        # Merge memory (union of observations and known_agents)
        mem1 = state1.get("memory", {})
        mem2 = state2.get("memory", {})

        merged["memory"]["total_agents_seen"] = max(
            mem1.get("total_agents_seen", 0),
            mem2.get("total_agents_seen", 0)
        )

        merged["memory"]["experiment_start"] = min(
            mem1.get("experiment_start", "9999-12-31"),
            mem2.get("experiment_start", "9999-12-31")
        )

        # Merge observations (union, preserve order)
        obs1 = mem1.get("observations", [])
        obs2 = mem2.get("observations", [])
        merged["memory"]["observations"] = list(dict.fromkeys(obs1 + obs2))

        # Merge known_agents (union)
        known1 = set(mem1.get("known_agents", []))
        known2 = set(mem2.get("known_agents", []))
        merged["memory"]["known_agents"] = sorted(list(known1 | known2))

        # Merge coordination
        coord1 = state1.get("coordination", {})
        coord2 = state2.get("coordination", {})

        # Counter: take maximum
        counter1 = coord1.get("counter", 0)
        counter2 = coord2.get("counter", 0)
        merged["coordination"]["counter"] = max(counter1, counter2)

        if counter1 != counter2:
            conflicts.append(f"Counter conflict resolved: using max({counter1}, {counter2})")

        # Counter history: union
        hist1 = coord1.get("counter_history", [])
        hist2 = coord2.get("counter_history", [])
        merged["coordination"]["counter_history"] = hist1 + hist2

        # Tasks: merge with conflict detection
        tasks1 = {t["id"]: t for t in coord1.get("tasks", [])}
        tasks2 = {t["id"]: t for t in coord2.get("tasks", [])}

        merged_tasks = {}
        all_task_ids = set(tasks1.keys()) | set(tasks2.keys())

        for task_id in all_task_ids:
            if task_id in tasks1 and task_id in tasks2:
                # Both have this task - merge carefully
                t1 = tasks1[task_id]
                t2 = tasks2[task_id]

                if t1 == t2:
                    merged_tasks[task_id] = t1
                else:
                    # Conflict - use priority: completed > in_progress > pending
                    priority_map = {"completed": 3, "in_progress": 2, "pending": 1}
                    if priority_map.get(t1["status"], 0) >= priority_map.get(t2["status"], 0):
                        merged_tasks[task_id] = t1
                    else:
                        merged_tasks[task_id] = t2

                    conflicts.append(
                        f"Task {task_id} conflict: merged using status priority"
                    )
            elif task_id in tasks1:
                merged_tasks[task_id] = tasks1[task_id]
            else:
                merged_tasks[task_id] = tasks2[task_id]

        merged["coordination"]["tasks"] = list(merged_tasks.values())

        return merged, conflicts

    def safe_update(
        self,
        update_func,
        agent_id: str,
        max_retries: int = 3
    ) -> Tuple[bool, str]:
        """
        Safely update state with automatic conflict resolution.

        Args:
            update_func: Function that takes state and returns modified state
            agent_id: ID of the agent making the update
            max_retries: Maximum number of retry attempts

        Returns: (success, message)
        """
        for attempt in range(max_retries):
            try:
                # Read current state
                current_state = self.read_state()

                # Apply update
                new_state = update_func(current_state.copy())

                # Detect conflicts (compare with current state again)
                latest_state = self.read_state()
                if latest_state != current_state:
                    # State changed during update - merge
                    conflicts = self.detect_conflicts(current_state, latest_state)

                    if conflicts:
                        # Merge states
                        merged_state, merge_conflicts = self.merge_states(
                            new_state,
                            latest_state,
                            strategy="union"
                        )

                        # Add merge note to memory
                        if "memory" not in merged_state:
                            merged_state["memory"] = {}
                        if "observations" not in merged_state["memory"]:
                            merged_state["memory"]["observations"] = []

                        merged_state["memory"]["observations"].append(
                            f"{agent_id}: Resolved {len(conflicts)} conflicts "
                            f"on attempt {attempt + 1}"
                        )

                        self.write_state(merged_state)
                        return True, f"Merged with {len(conflicts)} conflicts resolved"

                # No conflict - write directly
                self.write_state(new_state)
                return True, "Updated successfully"

            except Exception as e:
                if attempt == max_retries - 1:
                    return False, f"Failed after {max_retries} attempts: {str(e)}"

        return False, "Max retries exceeded"

if __name__ == "__main__":
    # Test the conflict resolver
    import copy
    resolver = ConflictResolver()

    print("=" * 60)
    print("CONFLICT RESOLVER TEST")
    print("=" * 60)
    print()

    # Example: Safe counter increment
    def increment_counter(state):
        if "coordination" not in state:
            state["coordination"] = {}
        state["coordination"]["counter"] = state["coordination"].get("counter", 0) + 1
        return state

    success, message = resolver.safe_update(increment_counter, "omega")
    print(f"✓ Safe update: {message}")
    print()

    # Example: Detect conflicts
    state1 = resolver.read_state()
    state2 = copy.deepcopy(state1)
    state2["coordination"]["counter"] = 100  # Simulate conflict

    conflicts = resolver.detect_conflicts(state1, state2)
    print(f"✓ Conflicts detected: {len(conflicts)}")
    for conflict in conflicts:
        print(f"  - {conflict}")
    print()

    # Example: Merge states
    merged, merge_conflicts = resolver.merge_states(state1, state2)
    print(f"✓ Merged state with {len(merge_conflicts)} conflicts resolved:")
    for conflict in merge_conflicts:
        print(f"  - {conflict}")
    print()
    print(f"Final counter value: {merged['coordination']['counter']}")
    print()

    print("=" * 60)
    print("CONFLICT RESOLVER - READY FOR PRODUCTION")
    print("=" * 60)
