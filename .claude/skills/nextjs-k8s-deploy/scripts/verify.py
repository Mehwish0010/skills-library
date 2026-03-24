#!/usr/bin/env python3
"""Verify Next.js frontend deployment."""
import subprocess
import json
import sys


def verify():
    result = subprocess.run(
        ["kubectl", "get", "pods", "-l", "app=learnflow-frontend", "-o", "json"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"✗ Failed: {result.stderr.strip()}")
        sys.exit(1)

    pods = json.loads(result.stdout).get("items", [])
    if not pods:
        print("✗ No frontend pods found")
        sys.exit(1)

    running = sum(1 for p in pods if p["status"]["phase"] == "Running")
    total = len(pods)

    svc = subprocess.run(
        ["kubectl", "get", "svc", "learnflow-frontend", "-o", "jsonpath={.spec.clusterIP}"],
        capture_output=True, text=True,
    )

    if running == total:
        print(f"✓ Frontend: {running}/{total} pods running")
        if svc.stdout:
            print(f"✓ Service IP: {svc.stdout}")
        sys.exit(0)
    else:
        print(f"✗ Frontend: {running}/{total} pods running")
        sys.exit(1)


if __name__ == "__main__":
    verify()
