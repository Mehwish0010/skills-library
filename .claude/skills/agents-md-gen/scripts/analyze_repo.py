#!/usr/bin/env python3
"""Analyze repository structure and output a summary for AGENTS.md generation."""
import os
import json
import sys


def analyze_repo(repo_path="."):
    result = {
        "directories": [],
        "key_files": [],
        "tech_indicators": [],
        "total_files": 0,
    }

    skip_dirs = {".git", "node_modules", "__pycache__", ".next", "venv", ".venv", "dist", "build"}

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        rel_root = os.path.relpath(root, repo_path)
        if rel_root == ".":
            rel_root = ""

        if rel_root:
            result["directories"].append(rel_root)

        for f in files:
            result["total_files"] += 1
            rel_path = os.path.join(rel_root, f) if rel_root else f

            if f == "package.json":
                result["tech_indicators"].append("Node.js")
            elif f in ("requirements.txt", "pyproject.toml"):
                result["tech_indicators"].append("Python")
            elif f == "Dockerfile":
                result["tech_indicators"].append("Docker")
            elif f in ("docker-compose.yml", "docker-compose.yaml"):
                result["tech_indicators"].append("Docker Compose")
            elif f.endswith((".yaml", ".yml")) and ("k8s" in rel_root or "kubernetes" in rel_root):
                result["tech_indicators"].append("Kubernetes")
            elif f == "go.mod":
                result["tech_indicators"].append("Go")

            if f in ("README.md", "AGENTS.md", "Dockerfile", "Makefile",
                      "package.json", "requirements.txt", "pyproject.toml",
                      "docker-compose.yml", ".env.example"):
                result["key_files"].append(rel_path)

    result["tech_indicators"] = list(set(result["tech_indicators"]))
    print(f"✓ Analyzed {result['total_files']} files in {len(result['directories'])} directories")
    print(f"  Tech stack: {', '.join(result['tech_indicators']) if result['tech_indicators'] else 'Unknown'}")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    analyze_repo(path)
