---
name: mcp-code-execution
description: Implement MCP with code execution pattern for token-efficient agent operations
---

# MCP Code Execution Pattern

## When to Use
- Wrapping MCP server calls in scripts for token efficiency
- Building skills that execute code instead of loading tools into context
- Reducing context window consumption from 41% to ~3%

## Instructions
1. Identify the MCP operation needed
2. Create a script wrapper: `python scripts/create_mcp_wrapper.py <operation-name>`
3. Test the wrapper: `python scripts/test_wrapper.py <operation-name>`
4. Integrate into a SKILL.md file

## Key Principle
- SKILL.md tells the agent WHAT to do (~100 tokens)
- scripts/*.py does the actual work (0 tokens - executed, not loaded)
- Only the final result enters context (minimal tokens)

## Validation
- [ ] Script executes successfully outside agent context
- [ ] Output is minimal and actionable
- [ ] No intermediate data enters context
- [ ] Token usage is under 200 for the full operation

See [REFERENCE.md](./REFERENCE.md) for patterns and examples.
