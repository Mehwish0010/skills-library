# AGENTS.md - Skills Library

## Project Overview
**skills-library** is a collection of reusable AI Skills with MCP Code Execution for building cloud-native applications. Skills work across Claude Code, Goose, and OpenAI Codex.

## Directory Structure
```
skills-library/
├── .claude/skills/          # All skills live here
│   ├── agents-md-gen/       # Generate AGENTS.md files
│   ├── kafka-k8s-setup/     # Deploy Kafka on Kubernetes
│   ├── postgres-k8s-setup/  # Deploy PostgreSQL on Kubernetes
│   ├── fastapi-dapr-agent/  # FastAPI + Dapr microservices
│   ├── mcp-code-execution/  # MCP code execution pattern
│   ├── nextjs-k8s-deploy/   # Deploy Next.js on Kubernetes
│   └── docusaurus-deploy/   # Deploy documentation site
├── docs/                    # Development guides
├── AGENTS.md                # This file
└── README.md                # Project overview
```

## Skill Structure Convention
Each skill follows this pattern:
```
skill-name/
├── SKILL.md         # Minimal instructions (~100 tokens)
├── REFERENCE.md     # Deep docs (loaded on-demand)
└── scripts/         # Executable scripts (0 tokens in context)
    ├── deploy.sh    # Deployment automation
    ├── verify.py    # Status verification
    └── *.py         # Additional automation
```

## Conventions & Patterns
- **SKILL.md**: YAML frontmatter with `name` and `description`, followed by When to Use, Instructions, and Validation sections
- **Scripts**: Python 3.12+ for verification, Bash for deployment. All scripts return minimal output (under 5 lines)
- **Token Efficiency**: Scripts execute outside agent context. Only final results enter context
- **Exit Codes**: 0 = success, 1 = failure
- **Output Format**: Use "✓" for success, "✗" for failure prefixes

## How to Use Skills
1. AI agent reads SKILL.md when triggered by user prompt
2. Agent executes scripts referenced in Instructions
3. Minimal output returns to agent context
4. Agent reports result to user

## Testing
- Each skill's verify.py can be run independently
- Test with: `python .claude/skills/<name>/scripts/verify.py`
