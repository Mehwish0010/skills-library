#!/usr/bin/env python3
"""Verify Kafka deployment status on Kubernetes."""
import subprocess
import json
import sys


def verify_kafka():
    result = subprocess.run(
        ["kubectl", "get", "pods", "-n", "kafka", "-o", "json"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"✗ Failed to get pods: {result.stderr.strip()}")
        sys.exit(1)

    pods = json.loads(result.stdout).get("items", [])
    if not pods:
        print("✗ No pods found in kafka namespace")
        sys.exit(1)

    running = sum(1 for p in pods if p["status"]["phase"] == "Running")
    total = len(pods)

    svc_result = subprocess.run(
        ["kubectl", "get", "svc", "-n", "kafka", "-o", "json"],
        capture_output=True, text=True,
    )
    services = json.loads(svc_result.stdout).get("items", [])
    svc_names = [s["metadata"]["name"] for s in services]

    if running == total:
        print(f"✓ All {total} Kafka pods running")
        print(f"✓ Services: {', '.join(svc_names)}")
        sys.exit(0)
    else:
        print(f"✗ {running}/{total} pods running")
        for p in pods:
            name = p["metadata"]["name"]
            phase = p["status"]["phase"]
            if phase != "Running":
                print(f"  - {name}: {phase}")
        sys.exit(1)


if __name__ == "__main__":
    verify_kafka()
