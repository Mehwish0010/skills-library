---
name: agents-md-gen
description: Generate AGENTS.md files that describe repository structure and conventions for AI coding agents
---

# AGENTS.md Generator

## When to Use
- Setting up a new repository for agentic development
- User asks to create or update an AGENTS.md file
- Onboarding AI agents to an existing codebase

## Instructions
1. Analyze the repository structure: `python scripts/analyze_repo.py`
2. Generate AGENTS.md: `python scripts/generate_agents_md.py`
3. Verify the output covers all required sections

## Validation
- [ ] AGENTS.md exists at repository root
- [ ] Contains project overview section
- [ ] Contains directory structure section
- [ ] Contains conventions and patterns section
- [ ] Contains setup instructions section

See [REFERENCE.md](./REFERENCE.md) for AGENTS.md format specification.
