# Tasks Directory

This directory contains task definitions for agent coordination.

## Task Format
Each task file should be named `task-{number}-{name}.json` and contain:
```json
{
  "id": "task-001",
  "title": "Task Title",
  "description": "Detailed description",
  "status": "open|claimed|in_progress|completed",
  "claimed_by": "agent_id",
  "created_at": "ISO timestamp",
  "updated_at": "ISO timestamp",
  "priority": "low|medium|high",
  "dependencies": []
}
```

## Available Tasks
Check individual task files for details.
