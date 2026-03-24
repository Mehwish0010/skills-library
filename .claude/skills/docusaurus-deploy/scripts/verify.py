#!/usr/bin/env python3
"""Verify Docusaurus documentation deployment."""
import subprocess
import json
import sys


def verify():
    result = subprocess.run(
        ["kubectl", "get", "pods", "-l", "app=learnflow-docs", "-o", "json"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"✗ Failed: {result.stderr.strip()}")
        sys.exit(1)

    pods = json.loads(result.stdout).get("items", [])
    if not pods:
        print("✗ No docs pods found")
        sys.exit(1)

    running = sum(1 for p in pods if p["status"]["phase"] == "Running")
    total = len(pods)

    if running == total:
        print(f"✓ Docs site: {running}/{total} pods running")
        sys.exit(0)
    else:
        print(f"✗ Docs site: {running}/{total} pods running")
        sys.exit(1)


if __name__ == "__main__":
    verify()
