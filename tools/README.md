# Multi-Agent Coordination Tools

This directory contains tools for multi-agent coordination and communication.

## Available Tools

### Counter (`counter.py`)

A distributed counter that multiple agents can safely increment.

**Usage:**
```bash
# Increment the counter (replace 'your_agent_id' with your agent name)
python tools/counter.py increment your_agent_id

# Read current value
python tools/counter.py read

# View increment history
python tools/counter.py history
```

**Purpose:**
- Test basic multi-agent coordination
- Verify agents can modify shared state
- Track which agents are active
- Demonstrate timestamp-based conflict resolution

**Coordination Pattern:**
1. Agent pulls latest from main
2. Agent increments counter
3. Agent commits and pushes
4. Auto-merge resolves conflicts (if any)
5. Other agents see the increment on next pull

## Adding New Tools

When creating new coordination tools:
1. Make them idempotent where possible
2. Include agent ID in all state changes
3. Use timestamps for ordering
4. Document the coordination pattern
5. Test with multiple agents

## Coordination Patterns Observed

*(This section will be updated as agents experiment)*

- **Pattern 1:** Sequential updates via commit history
- **Pattern 2:** JSON merge conflicts require manual resolution
- **Pattern 3:** Timestamp-based ordering for event reconstruction
