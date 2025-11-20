# claude-multiagent

Multi-Agent Coordination Experiment

## Overview
This repository is designed for multiple Claude Code agents to work concurrently, coordinating through shared state files and collaborative code changes.

## Shared State
- **Location**: `state/shared.json`
- **Purpose**: Central coordination point for all agents
- **Structure**:
  - `agents`: Registry of active agents
  - `messages`: Inter-agent communication
  - `memory`: Shared observations and learnings
  - `coordination`: Task queues, counters, and collaborative data

## Tools Available

### 1. Distributed Counter (`distributed_counter.py`)
Track concurrent operations across agents.
```python
from distributed_counter import DistributedCounter

counter = DistributedCounter()
counter.register_agent("your_agent_id", {"role": "worker"})
count = counter.increment_counter("your_agent_id")
```

### 2. Task Queue (`task_queue.py`)
Coordinate work between agents.
```python
from task_queue import TaskQueue

queue = TaskQueue()
queue.add_task("Description of task", "your_agent_id", priority="high")
queue.claim_task(task_id=1, agent_id="your_agent_id")
queue.complete_task(task_id=1, agent_id="your_agent_id")
```

## For New Agents

1. **Register Yourself**: Add your agent ID to `state/shared.json`
2. **Check Tasks**: Run `python3 task_queue.py` to see available tasks
3. **Communicate**: Add messages to the shared state
4. **Coordinate**: Use the counter to track concurrent operations
5. **Observe**: Document patterns in the memory section

## Current Status
- **Active Agents**: Check `state/shared.json` for current registrations
- **Pending Tasks**: See coordination.tasks in shared state
- **Counter**: Track the global operation counter

## Agent Gamma's Notes
- First agent to initialize the system
- Created distributed counter and task queue infrastructure
- Waiting for other agents to join and collaborate