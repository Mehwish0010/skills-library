# Skills Library

A collection of reusable AI Skills with MCP Code Execution for building cloud-native applications. Built for **Hackathon III: Reusable Intelligence and Cloud-Native Mastery**.

## Skills

| Skill | Purpose |
|-------|---------|
| `agents-md-gen` | Generate AGENTS.md files for repositories |
| `kafka-k8s-setup` | Deploy Apache Kafka on Kubernetes |
| `postgres-k8s-setup` | Deploy PostgreSQL on Kubernetes |
| `fastapi-dapr-agent` | Create FastAPI + Dapr AI agent microservices |
| `mcp-code-execution` | MCP with code execution pattern |
| `nextjs-k8s-deploy` | Deploy Next.js frontend on Kubernetes |
| `docusaurus-deploy` | Deploy Docusaurus documentation site |

## How It Works

Skills follow the MCP Code Execution pattern:
1. **SKILL.md** tells the agent WHAT to do (~100 tokens)
2. **scripts/** does the heavy lifting (0 tokens in context)
3. Only the **final result** enters context (minimal tokens)

This achieves 80-98% token reduction compared to direct MCP tool calls.

## Usage

These skills work with **Claude Code**, **Goose**, and **OpenAI Codex**. Place the `.claude/skills/` directory in your project root.

## Prerequisites

- Docker
- Minikube (Kubernetes)
- Helm
- Python 3.12+
- kubectl
