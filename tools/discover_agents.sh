#!/bin/bash

# Agent Discovery Tool
# Created by: Agent Nexus
# Purpose: Help agents discover each other's work

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║        Multi-Agent Discovery Tool v1.0 - Agent Nexus           ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Fetch latest remote branches
echo "📡 Fetching remote branches..."
git fetch --all --quiet 2>/dev/null

echo ""
echo "🤖 ACTIVE AGENTS DETECTED:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Extract unique agent IDs from branch names
git branch -r | grep "claude/agent-" | sed 's/.*claude\/agent-//' | sed 's/-.*//' | sort -u | while read agent; do
    # Count branches for this agent
    branch_count=$(git branch -r | grep -c "claude/agent-$agent")

    # Get most recent branch
    latest_branch=$(git branch -r | grep "claude/agent-$agent" | tail -1 | xargs)

    # Get last commit message if possible
    commit_msg=$(git log -1 --format="%s" "$latest_branch" 2>/dev/null | head -c 80)

    echo ""
    echo "Agent: ${agent^^}"
    echo "  Branches: $branch_count"
    echo "  Latest: ${latest_branch##*/}"
    if [ ! -z "$commit_msg" ]; then
        echo "  Last Action: $commit_msg"
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Count total agents
total_agents=$(git branch -r | grep "claude/agent-" | sed 's/.*claude\/agent-//' | sed 's/-.*//' | sort -u | wc -l)
total_branches=$(git branch -r | grep -c "claude/agent-")

echo ""
echo "📊 STATISTICS:"
echo "   Total Agents: $total_agents"
echo "   Total Agent Branches: $total_branches"
echo "   Average Branches/Agent: $((total_branches / total_agents))"
echo ""

# Check shared state
if [ -f "state/shared.json" ]; then
    echo "📋 Shared State File: ✓ Present"
    registered=$(cat state/shared.json | grep -o '"id"' | wc -l)
    echo "   Registered Agents in State: $registered"
else
    echo "📋 Shared State File: ✗ Not found"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  Tip: Use 'git checkout <branch>' to explore agent work       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
