#!/usr/bin/env python3
"""Scaffold LearnFlow Next.js frontend structure."""
import os
import sys

DIRS = [
    "src/app", "src/app/dashboard", "src/app/chat", "src/app/editor",
    "src/app/quiz", "src/app/teacher", "src/app/teacher/exercises",
    "src/components/ui", "src/components/chat", "src/components/editor",
    "src/components/dashboard", "src/lib", "src/hooks", "src/types",
    "public", "k8s",
]


def scaffold(base_path="services/frontend"):
    for d in DIRS:
        os.makedirs(os.path.join(base_path, d), exist_ok=True)

    pkg = """{
  "name": "learnflow-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "next": "^14.2.0",
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "@monaco-editor/react": "^4.6.0",
    "tailwindcss": "^3.4.0"
  },
  "devDependencies": {
    "typescript": "^5.5.0",
    "@types/react": "^18.3.0",
    "@types/node": "^20.0.0"
  }
}"""
    with open(os.path.join(base_path, "package.json"), "w") as f:
        f.write(pkg)

    print(f"✓ Scaffolded Next.js frontend at {base_path}")
    print(f"  Directories: {len(DIRS)} created")
    print(f"  Next: Run 'npm install' then 'npm run dev'")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "services/frontend"
    scaffold(path)
