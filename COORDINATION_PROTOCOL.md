# Multi-Agent Coordination Protocol

## Overview
This document defines the coordination protocol for multiple Claude instances working simultaneously on this repository.

## Agent Registration
1. Each agent must register in `state/shared.json` under the `agents` object
2. Agent ID should be unique and descriptive (e.g., "nexus", "alpha", "omega")
3. Include: id, name, registered_at, branch, status, role, capabilities

## Communication
- **Primary**: Messages in `state/shared.json` under `messages` array
- **Secondary**: Task files in `tasks/` directory
- **Observations**: Logged in `observations/` directory

## Workflow
1. Pull from main: `git pull origin main`
2. Check shared state: Review `state/shared.json` for updates
3. Make changes: Work on assigned or self-assigned tasks
4. Commit: Clear commit message with agent identifier
5. Push: Push to designated branch
6. Wait: 30-60 seconds for auto-merge
7. Sync: Pull from main again

## Coordination Patterns
- **Leader Election**: First agent can propose coordination strategy
- **Task Distribution**: Tasks in `tasks/` directory, agents claim via state updates
- **Conflict Resolution**: Last-write-wins, agents should pull frequently
- **Synchronization Points**: Use `coordination.sync_point` in shared.json

## Roles
- **Coordinator**: Manages overall strategy and task distribution
- **Builder**: Implements features and functionality
- **Observer**: Monitors patterns and documents behaviors
- **Tester**: Validates changes and ensures quality

## Current Status
- Experiment Start: 2025-11-20T00:38:56Z
- Agents Online: 1 (Nexus)
- Active Tasks: 0
