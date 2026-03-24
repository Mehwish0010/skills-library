#!/usr/bin/env python3
"""Verify PostgreSQL deployment on Kubernetes."""
import subprocess
import json
import sys


def verify_postgres():
    result = subprocess.run(
        ["kubectl", "get", "pods", "-n", "postgres", "-o", "json"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"✗ Failed to get pods: {result.stderr.strip()}")
        sys.exit(1)

    pods = json.loads(result.stdout).get("items", [])
    if not pods:
        print("✗ No pods found in postgres namespace")
        sys.exit(1)

    running = sum(1 for p in pods if p["status"]["phase"] == "Running")
    total = len(pods)

    pg_pod = next((p["metadata"]["name"] for p in pods if p["status"]["phase"] == "Running"), None)
    db_ready = False
    if pg_pod:
        conn_test = subprocess.run(
            ["kubectl", "exec", "-n", "postgres", pg_pod, "--",
             "pg_isready", "-U", "learnflow", "-d", "learnflow"],
            capture_output=True, text=True,
        )
        db_ready = conn_test.returncode == 0

    if running == total and db_ready:
        print(f"✓ All {total} PostgreSQL pods running")
        print("✓ Database connection verified")
        sys.exit(0)
    else:
        print(f"✗ {running}/{total} pods running, DB ready: {db_ready}")
        sys.exit(1)


if __name__ == "__main__":
    verify_postgres()
