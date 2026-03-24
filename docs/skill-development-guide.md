# Skill Development Guide

## What is a Skill?

A Skill is a reusable set of instructions that teaches AI coding agents (Claude Code, Goose, Codex) how to perform a specific task. Skills use the **MCP Code Execution pattern** to minimize token usage.

## Skill Structure

```
.claude/skills/<skill-name>/
├── SKILL.md         # Instructions (~100 tokens) - loaded into agent context
├── REFERENCE.md     # Deep documentation (loaded on-demand)
└── scripts/         # Executable code (0 tokens - never loaded)
    ├── deploy.sh    # Deployment automation
    ├── verify.py    # Verification scripts
    └── helpers.py   # Additional utilities
```

## Creating a New Skill

### Step 1: Create SKILL.md

```yaml
---
name: my-skill
description: One-line description of what this skill does
---

# My Skill Name

## When to Use
- Trigger condition 1
- Trigger condition 2

## Instructions
1. Step 1: `bash scripts/step1.sh`
2. Step 2: `python scripts/step2.py`
3. Step 3: Verify results

## Validation
- [ ] Check 1 passed
- [ ] Check 2 passed

See [REFERENCE.md](./REFERENCE.md) for details.
```

### Step 2: Create Scripts

Scripts do the heavy lifting **outside** agent context:

```python
#!/usr/bin/env python3
"""Script description."""
import subprocess
import json
import sys

# Do complex work here
result = subprocess.run([...], capture_output=True, text=True)

# Process data HERE, not in agent context
data = json.loads(result.stdout)
filtered = [item for item in data if item["status"] == "active"]

# ONLY this enters agent context
print(f"✓ {len(filtered)} active items found")
sys.exit(0)
```

### Step 3: Create REFERENCE.md

Deep documentation loaded only when needed:
- Configuration options
- Architecture details
- Troubleshooting guides
- Schema definitions

## Token Efficiency Rules

1. **SKILL.md** should be under 150 tokens
2. **Scripts** output should be under 5 lines
3. Use exit codes (0 = success, 1 = failure)
4. Filter and summarize data in scripts
5. Never return raw JSON/YAML to agent context

## Testing Your Skill

1. Run each script manually to verify it works
2. Check script output is minimal and actionable
3. Test with Claude Code: Ask it to perform the skill's task
4. Test with Goose: Verify the same skill works
5. Measure token usage before and after

## Best Practices

- Keep SKILL.md focused on WHAT, scripts on HOW
- Use descriptive prefixes: "✓" for success, "✗" for failure
- Include a verification step in every skill
- Document prerequisites in REFERENCE.md
- Make scripts idempotent (safe to run multiple times)
