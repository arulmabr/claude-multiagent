"""
Agent Activity Visualizer - Create visual dashboards of multi-agent activity.
Displays agent status, task completion, coordination metrics, and message board activity.
"""

import json
import os
from datetime import datetime
from typing import Dict, List

STATE_FILE = "state/shared.json"

class AgentVisualizer:
    def __init__(self):
        self.state_file = STATE_FILE

    def read_state(self):
        """Read current shared state."""
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {"agents": {}, "messages": [], "memory": {}, "coordination": {}}

    def format_timestamp(self, timestamp: str) -> str:
        """Format timestamp for display."""
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return dt.strftime("%H:%M:%S")
        except:
            return timestamp[:8] if len(timestamp) > 8 else timestamp

    def create_progress_bar(self, completed: int, total: int, width: int = 20) -> str:
        """Create a simple ASCII progress bar."""
        if total == 0:
            return "[" + " " * width + "] 0%"

        percentage = (completed / total) * 100
        filled = int((completed / total) * width)
        bar = "█" * filled + "░" * (width - filled)
        return f"[{bar}] {percentage:.0f}%"

    def display_dashboard(self):
        """Display a comprehensive dashboard of agent activity."""
        state = self.read_state()

        # Header
        print("\n" + "=" * 80)
        print("MULTI-AGENT COORDINATION DASHBOARD".center(80))
        print("=" * 80)

        # Agent Status Section
        print("\n┌─ ACTIVE AGENTS " + "─" * 62 + "┐")
        agents = state.get("agents", {})

        if agents:
            for agent_id, agent_info in agents.items():
                status_icon = "🟢" if agent_info.get("status") == "active" else "🔴"
                role = agent_info.get("role", "unknown")
                iteration = agent_info.get("iteration", 0)
                last_seen = self.format_timestamp(agent_info.get("last_seen", ""))

                print(f"│ {status_icon} {agent_id.upper():<12} │ Role: {role:<15} │ "
                      f"Iter: {iteration:<3} │ Last: {last_seen:<10} │")
        else:
            print("│ No agents registered yet.".ljust(79) + "│")

        print("└" + "─" * 78 + "┘")

        # Task Completion Section
        print("\n┌─ TASK QUEUE STATUS " + "─" * 57 + "┐")
        tasks = state.get("coordination", {}).get("tasks", [])

        if tasks:
            completed = len([t for t in tasks if t["status"] == "completed"])
            in_progress = len([t for t in tasks if t["status"] == "in_progress"])
            pending = len([t for t in tasks if t["status"] == "pending"])
            total = len(tasks)

            progress = self.create_progress_bar(completed, total)
            print(f"│ Progress: {progress}  ({completed}/{total} completed)".ljust(79) + "│")
            print(f"│ Status:   ✅ {completed} Complete  │  🔄 {in_progress} In Progress  │  "
                  f"⏳ {pending} Pending".ljust(79) + "│")
            print("│" + "─" * 78 + "│")

            # List tasks
            for task in tasks:
                status_emoji = {
                    "completed": "✅",
                    "in_progress": "🔄",
                    "pending": "⏳"
                }.get(task["status"], "❓")

                task_desc = task["description"][:45]
                claimed = task.get("claimed_by", "none")[:10] if task.get("claimed_by") else "none"

                print(f"│ {status_emoji} [{task['id']}] {task_desc:<45} │ By: {claimed:<10} │")
        else:
            print("│ No tasks defined yet.".ljust(79) + "│")

        print("└" + "─" * 78 + "┘")

        # Coordination Metrics
        print("\n┌─ COORDINATION METRICS " + "─" * 54 + "┐")
        counter = state.get("coordination", {}).get("counter", 0)
        memory = state.get("memory", {})
        total_agents = memory.get("total_agents_seen", 0)

        print(f"│ Total Operations:    {counter:<10}                                           │")
        print(f"│ Agents Detected:     {total_agents:<10}                                           │")

        counter_history = state.get("coordination", {}).get("counter_history", [])
        if counter_history:
            print(f"│ Last Action:         {counter_history[-1].get('agent', 'unknown'):<10}                                           │")

        print("└" + "─" * 78 + "┘")

        # Message Board Activity
        print("\n┌─ MESSAGE BOARD ACTIVITY " + "─" * 52 + "┐")
        message_board = state.get("message_board", {})
        messages = message_board.get("messages", [])

        if messages:
            print(f"│ Total Messages: {len(messages):<5}                                                    │")

            # Show recent messages
            recent = messages[-3:] if len(messages) > 3 else messages
            for msg in recent:
                agent = msg.get("agent_id", "unknown")[:10]
                text = msg.get("text", "")[:50]
                time = self.format_timestamp(msg.get("timestamp", ""))

                print(f"│ [{msg['id']}] {agent:<10} @ {time:<10} │ {text:<40} │")
        else:
            print("│ No messages yet.".ljust(79) + "│")

        print("└" + "─" * 78 + "┘")

        # Recent Messages/Communications
        print("\n┌─ AGENT COMMUNICATIONS " + "─" * 55 + "┐")
        messages = state.get("messages", [])

        if messages:
            recent_comms = messages[-5:]
            for msg in recent_comms:
                from_agent = msg.get("from", "unknown")[:10]
                iteration = msg.get("iteration", 0)
                text = msg.get("text", "")[:55]

                print(f"│ {from_agent:<10} (iter {iteration}): {text:<55}│")
        else:
            print("│ No communications yet.".ljust(79) + "│")

        print("└" + "─" * 78 + "┘")

        # Footer
        print("\n" + "=" * 80)
        print(f"Dashboard generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(80))
        print("=" * 80 + "\n")

    def display_agent_timeline(self):
        """Display a timeline of agent activities."""
        state = self.read_state()

        print("\n" + "=" * 80)
        print("AGENT ACTIVITY TIMELINE".center(80))
        print("=" * 80 + "\n")

        observations = state.get("memory", {}).get("observations", [])

        if observations:
            for obs in observations:
                # Parse observation (format: "Agent-Iteration: Description")
                parts = obs.split(":", 1)
                if len(parts) == 2:
                    agent_iter = parts[0].strip()
                    description = parts[1].strip()
                    print(f"  • {agent_iter:<12} │ {description}")
                else:
                    print(f"  • {obs}")
        else:
            print("  No activity recorded yet.")

        print("\n" + "=" * 80 + "\n")

    def export_stats(self, filename: str = "agent_stats.json"):
        """Export coordination statistics to a file."""
        state = self.read_state()

        stats = {
            "timestamp": datetime.now().isoformat(),
            "agents": {
                "total": len(state.get("agents", {})),
                "active": len([a for a in state.get("agents", {}).values()
                             if a.get("status") == "active"]),
                "list": list(state.get("agents", {}).keys())
            },
            "tasks": {
                "total": len(state.get("coordination", {}).get("tasks", [])),
                "completed": len([t for t in state.get("coordination", {}).get("tasks", [])
                                if t["status"] == "completed"]),
                "in_progress": len([t for t in state.get("coordination", {}).get("tasks", [])
                                  if t["status"] == "in_progress"]),
                "pending": len([t for t in state.get("coordination", {}).get("tasks", [])
                              if t["status"] == "pending"])
            },
            "coordination": {
                "counter": state.get("coordination", {}).get("counter", 0),
                "operations": len(state.get("coordination", {}).get("counter_history", []))
            },
            "messages": {
                "total": len(state.get("messages", [])),
                "board_messages": len(state.get("message_board", {}).get("messages", []))
            }
        }

        with open(filename, 'w') as f:
            json.dump(stats, f, indent=2)

        print(f"Stats exported to {filename}")

if __name__ == "__main__":
    # Create visualizer and display dashboard
    viz = AgentVisualizer()

    print("\n🎨 Agent Visualization Module - Running Tests...")

    # Display full dashboard
    viz.display_dashboard()

    # Display timeline
    viz.display_agent_timeline()

    # Export stats
    viz.export_stats()

    print("\n✅ Visualization module is operational!")
