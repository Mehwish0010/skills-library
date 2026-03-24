# MCP Code Execution Pattern Reference

## The Problem
Direct MCP tool calls load all tool definitions into context at startup:
- 1 server (5 tools) = ~10,000 tokens
- 3 servers (15 tools) = ~30,000 tokens
- 5 servers (25 tools) = ~50,000+ tokens

## The Solution
Wrap MCP operations in executable scripts:
1. Agent reads SKILL.md (~100 tokens)
2. Agent executes script (0 tokens loaded)
3. Script calls MCP server directly
4. Only minimal output returns to context (~10 tokens)

Result: 80-98% token reduction while maintaining full capability.

## Pattern Template
```python
#!/usr/bin/env python3
"""MCP wrapper - executes outside agent context."""
import subprocess
import json

# Do the heavy lifting here
result = call_mcp_operation()

# Filter/process data here
filtered = process(result)

# Only this enters agent context
print(f"✓ {len(filtered)} items processed")
```

## Before vs After

### Before (Direct MCP - 50,000 tokens)
```
TOOL CALL: k8s.getPods(namespace: "default")
→ returns full pod JSON (25,000 tokens into context)
```

### After (Script Execution - 10 tokens)
```python
result = subprocess.run(["kubectl", "get", "pods", "-o", "json"], ...)
pods = json.loads(result.stdout)["items"]
running = sum(1 for p in pods if p["status"]["phase"] == "Running")
print(f"✓ {running}/{len(pods)} pods running")
```

## Best Practices
1. Always filter data in the script, not in the agent
2. Return counts, statuses, and summaries - not raw data
3. Use exit codes for pass/fail (0 = success, 1 = failure)
4. Log details to files if debugging is needed
5. Keep script output under 5 lines
