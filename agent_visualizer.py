"""
Agent Visualizer - Real-time visualization of multi-agent activity.
Generates reports and activity summaries for agent coordination.
"""

import json
import os
from datetime import datetime
from collections import defaultdict

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

    def generate_summary(self):
        """Generate a comprehensive summary of agent activity."""
        state = self.read_state()
        agents = state.get("agents", {})
        messages = state.get("messages", [])
        coordination = state.get("coordination", {})
        memory = state.get("memory", {})

        summary = []
        summary.append("=" * 60)
        summary.append("MULTI-AGENT COORDINATION DASHBOARD")
        summary.append("=" * 60)
        summary.append("")

        # Agent Overview
        summary.append(f"Active Agents: {len(agents)}")
        summary.append(f"Total Counter: {coordination.get('counter', 0)}")
        summary.append(f"Total Messages: {len(messages)}")
        summary.append("")

        # Agent Details
        summary.append("REGISTERED AGENTS:")
        summary.append("-" * 60)
        for agent_id, agent_data in agents.items():
            summary.append(f"  [{agent_id.upper()}]")
            summary.append(f"    Role: {agent_data.get('role', 'unknown')}")
            summary.append(f"    Joined: {agent_data.get('joined_at', 'unknown')}")
            summary.append(f"    Branch: {agent_data.get('branch', 'unknown')[:50]}...")
            summary.append(f"    Status: {agent_data.get('status', 'unknown')}")
            summary.append("")

        # Task Summary
        tasks = coordination.get("tasks", [])
        if tasks:
            summary.append("TASK PROGRESS:")
            summary.append("-" * 60)
            completed = sum(1 for t in tasks if t.get("status") == "completed")
            in_progress = sum(1 for t in tasks if t.get("status") == "in_progress")
            pending = sum(1 for t in tasks if t.get("status") == "pending")

            summary.append(f"  Completed: {completed}")
            summary.append(f"  In Progress: {in_progress}")
            summary.append(f"  Pending: {pending}")
            summary.append(f"  Total: {len(tasks)}")
            summary.append("")

            for task in tasks:
                status_icon = "✓" if task.get("status") == "completed" else "⧗" if task.get("status") == "in_progress" else "○"
                summary.append(f"  {status_icon} Task #{task.get('id')}: {task.get('description')}")
                summary.append(f"    Status: {task.get('status')}")
                if task.get("claimed_by"):
                    summary.append(f"    Claimed by: {task.get('claimed_by')}")
                if task.get("completed_by"):
                    summary.append(f"    Completed by: {task.get('completed_by')}")
                summary.append("")

        # Message Activity
        summary.append("MESSAGE ACTIVITY:")
        summary.append("-" * 60)

        # Count messages per agent
        msg_counts = defaultdict(int)
        for msg in messages:
            msg_counts[msg.get("from", "unknown")] += 1

        for agent, count in sorted(msg_counts.items()):
            summary.append(f"  {agent}: {count} messages")
        summary.append("")

        # Recent messages
        summary.append("RECENT MESSAGES (last 5):")
        summary.append("-" * 60)
        recent_messages = messages[-5:] if len(messages) > 5 else messages
        for msg in recent_messages:
            sender = msg.get("from", "unknown")
            text = msg.get("text", "")
            timestamp = msg.get("timestamp", "")
            priority = msg.get("priority", "normal")
            priority_flag = "[HIGH]" if priority == "high" else ""

            summary.append(f"  [{sender}] {priority_flag}")
            summary.append(f"    {text[:80]}...")
            if timestamp:
                summary.append(f"    @ {timestamp}")
            summary.append("")

        # Counter History
        counter_history = coordination.get("counter_history", [])
        if counter_history:
            summary.append("COUNTER HISTORY:")
            summary.append("-" * 60)
            for entry in counter_history:
                summary.append(f"  {entry.get('agent')} -> {entry.get('value')} @ {entry.get('timestamp')}")
            summary.append("")

        # Observations
        observations = memory.get("observations", [])
        if observations:
            summary.append("KEY OBSERVATIONS:")
            summary.append("-" * 60)
            for obs in observations[-5:]:  # Last 5 observations
                summary.append(f"  • {obs}")
            summary.append("")

        summary.append("=" * 60)
        summary.append(f"Generated: {datetime.now().isoformat()}")
        summary.append("=" * 60)

        return "\n".join(summary)

    def generate_activity_matrix(self):
        """Generate an activity matrix showing agent interactions."""
        state = self.read_state()
        agents = list(state.get("agents", {}).keys())
        messages = state.get("messages", [])

        matrix = []
        matrix.append("\nAGENT ACTIVITY MATRIX")
        matrix.append("-" * 40)

        # Create message flow visualization
        for agent in agents:
            agent_messages = [m for m in messages if m.get("from") == agent]
            matrix.append(f"{agent:>8}: {'█' * len(agent_messages)}")

        return "\n".join(matrix)

    def export_html_report(self, filename="agent_report.html"):
        """Generate an HTML report (basic version)."""
        state = self.read_state()

        html = """
<!DOCTYPE html>
<html>
<head>
    <title>Multi-Agent Coordination Report</title>
    <style>
        body {{ font-family: monospace; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; }}
        h1 {{ color: #333; border-bottom: 2px solid #333; }}
        .agent {{ background: #e8f4f8; padding: 10px; margin: 10px 0; border-radius: 5px; }}
        .task {{ padding: 8px; margin: 5px 0; border-left: 3px solid #ccc; }}
        .completed {{ border-left-color: green; }}
        .in-progress {{ border-left-color: orange; }}
        .pending {{ border-left-color: gray; }}
        .message {{ background: #f9f9f9; padding: 8px; margin: 5px 0; border-radius: 3px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Multi-Agent Coordination Report</h1>
        <p>Generated: {timestamp}</p>

        <h2>Agents ({agent_count})</h2>
        {agents_html}

        <h2>Tasks</h2>
        {tasks_html}

        <h2>Messages</h2>
        {messages_html}
    </div>
</body>
</html>
""".format(
            timestamp=datetime.now().isoformat(),
            agent_count=len(state.get("agents", {})),
            agents_html=self._generate_agents_html(state),
            tasks_html=self._generate_tasks_html(state),
            messages_html=self._generate_messages_html(state)
        )

        with open(filename, 'w') as f:
            f.write(html)

        return filename

    def _generate_agents_html(self, state):
        agents = state.get("agents", {})
        html_parts = []
        for agent_id, agent_data in agents.items():
            html_parts.append(f"""
                <div class="agent">
                    <strong>{agent_id.upper()}</strong><br/>
                    Role: {agent_data.get('role', 'unknown')}<br/>
                    Status: {agent_data.get('status', 'unknown')}<br/>
                    Joined: {agent_data.get('joined_at', 'unknown')}
                </div>
            """)
        return "".join(html_parts)

    def _generate_tasks_html(self, state):
        tasks = state.get("coordination", {}).get("tasks", [])
        html_parts = []
        for task in tasks:
            status = task.get("status", "pending")
            html_parts.append(f"""
                <div class="task {status}">
                    <strong>Task #{task.get('id')}: {task.get('description')}</strong><br/>
                    Status: {status}<br/>
                    {f"Claimed by: {task.get('claimed_by')}<br/>" if task.get('claimed_by') else ""}
                    {f"Completed by: {task.get('completed_by')}<br/>" if task.get('completed_by') else ""}
                </div>
            """)
        return "".join(html_parts)

    def _generate_messages_html(self, state):
        messages = state.get("messages", [])
        html_parts = []
        for msg in messages[-10:]:  # Last 10 messages
            html_parts.append(f"""
                <div class="message">
                    <strong>[{msg.get('from')}]</strong> {msg.get('text', '')}<br/>
                    <small>{msg.get('timestamp', '')}</small>
                </div>
            """)
        return "".join(html_parts)

if __name__ == "__main__":
    visualizer = AgentVisualizer()

    # Generate text summary
    print(visualizer.generate_summary())
    print(visualizer.generate_activity_matrix())

    # Generate HTML report
    html_file = visualizer.export_html_report()
    print(f"\nHTML report generated: {html_file}")
