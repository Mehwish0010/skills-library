#!/usr/bin/env python3
"""Scaffold Docusaurus documentation site."""
import os
import sys

DIRS = [
    "docs/getting-started", "docs/architecture", "docs/skills",
    "docs/api", "src/pages", "static/img", "k8s",
]


def scaffold(base_path="docs-site"):
    for d in DIRS:
        os.makedirs(os.path.join(base_path, d), exist_ok=True)

    intro = """---
sidebar_position: 1
---

# LearnFlow Documentation

Welcome to the LearnFlow documentation. LearnFlow is an AI-powered Python tutoring platform.

## Quick Start
1. Set up your development environment
2. Deploy infrastructure (Kafka, PostgreSQL)
3. Deploy backend services
4. Deploy frontend
5. Start learning!

## Architecture
LearnFlow uses a microservices architecture with:
- **Next.js Frontend** - Student and teacher dashboards
- **FastAPI Backend** - AI-powered tutoring agents
- **Kafka** - Event-driven messaging
- **Dapr** - Service mesh for state and pub/sub
- **PostgreSQL** - Persistent data storage
- **MCP Servers** - AI context providers
"""
    with open(os.path.join(base_path, "docs", "intro.md"), "w") as f:
        f.write(intro)

    pkg = """{
  "name": "learnflow-docs",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "docusaurus": "docusaurus",
    "start": "docusaurus start",
    "build": "docusaurus build",
    "serve": "docusaurus serve"
  },
  "dependencies": {
    "@docusaurus/core": "^3.5.0",
    "@docusaurus/preset-classic": "^3.5.0",
    "react": "^18.3.0",
    "react-dom": "^18.3.0"
  }
}"""
    with open(os.path.join(base_path, "package.json"), "w") as f:
        f.write(pkg)

    print(f"✓ Scaffolded Docusaurus site at {base_path}")
    print(f"  Directories: {len(DIRS)} created")
    print(f"  Next: Run 'npm install' then 'npm start'")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "docs-site"
    scaffold(path)
