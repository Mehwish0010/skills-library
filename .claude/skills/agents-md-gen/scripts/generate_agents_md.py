#!/usr/bin/env python3
"""Generate an AGENTS.md file based on repository analysis."""
import os
import json
import sys


def get_tree(path=".", prefix="", max_depth=3, current_depth=0):
    if current_depth >= max_depth:
        return ""
    skip_dirs = {".git", "node_modules", "__pycache__", ".next", "venv", ".venv", "dist", "build"}
    lines = []
    try:
        entries = sorted(os.listdir(path))
    except PermissionError:
        return ""
    dirs = [e for e in entries if os.path.isdir(os.path.join(path, e)) and e not in skip_dirs]
    files = [e for e in entries if os.path.isfile(os.path.join(path, e))]
    all_entries = dirs + files
    for i, entry in enumerate(all_entries):
        connector = "└── " if i == len(all_entries) - 1 else "├── "
        lines.append(f"{prefix}{connector}{entry}")
        if entry in dirs:
            extension = "    " if i == len(all_entries) - 1 else "│   "
            subtree = get_tree(os.path.join(path, entry), prefix + extension, max_depth, current_depth + 1)
            if subtree:
                lines.append(subtree)
    return "\n".join(lines)


def detect_tech_stack(path="."):
    stack = []
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in {".git", "node_modules", "__pycache__"}]
        for f in files:
            if f == "package.json":
                try:
                    with open(os.path.join(root, f)) as fh:
                        pkg = json.load(fh)
                        deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
                        if "next" in deps:
                            stack.append("Next.js")
                        if "react" in deps:
                            stack.append("React")
                        if "typescript" in deps:
                            stack.append("TypeScript")
                except Exception:
                    pass
            elif f == "requirements.txt":
                stack.append("Python")
                try:
                    with open(os.path.join(root, f)) as fh:
                        content = fh.read()
                        if "fastapi" in content.lower():
                            stack.append("FastAPI")
                        if "dapr" in content.lower():
                            stack.append("Dapr")
                except Exception:
                    pass
            elif f == "Dockerfile":
                stack.append("Docker")
    return list(set(stack))


def generate_agents_md(repo_path="."):
    repo_name = os.path.basename(os.path.abspath(repo_path))
    tree = get_tree(repo_path)
    tech_stack = detect_tech_stack(repo_path)

    content = f"""# AGENTS.md - {repo_name}

## Project Overview
**{repo_name}** is a project using: {', '.join(tech_stack) if tech_stack else 'See below'}.

## Directory Structure
```
{repo_name}/
{tree}
```

## Conventions & Patterns
- Follow existing code style and naming conventions
- Use descriptive variable and function names
- Handle errors gracefully with proper logging
- Write tests for new functionality

## Development Setup
1. Clone the repository
2. Install dependencies
3. Set up environment variables (copy .env.example to .env)
4. Run the development server

## Testing
- Run tests before submitting changes
- Maintain test coverage for critical paths

## Key Files
- `AGENTS.md` - This file (AI agent guidelines)
- `README.md` - Project documentation
"""

    output_path = os.path.join(repo_path, "AGENTS.md")
    with open(output_path, "w") as f:
        f.write(content)

    print(f"✓ Generated AGENTS.md at {output_path}")
    print(f"  Tech stack: {', '.join(tech_stack) if tech_stack else 'None detected'}")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    generate_agents_md(path)
