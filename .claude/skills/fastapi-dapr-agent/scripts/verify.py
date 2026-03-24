#!/usr/bin/env python3
"""Verify a FastAPI service deployment."""
import subprocess
import json
import sys


def verify_service(service_name):
    result = subprocess.run(
        ["kubectl", "get", "pods", "-l", f"app={service_name}", "-o", "json"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"✗ Failed to get pods: {result.stderr.strip()}")
        sys.exit(1)

    pods = json.loads(result.stdout).get("items", [])
    if not pods:
        print(f"✗ No pods found for {service_name}")
        sys.exit(1)

    running = sum(1 for p in pods if p["status"]["phase"] == "Running")
    total = len(pods)

    has_dapr = any(
        "daprd" in [c["name"] for c in p["spec"]["containers"]]
        for p in pods
    )

    if running == total:
        print(f"✓ {service_name}: {running}/{total} pods running")
        print(f"✓ Dapr sidecar: {'Yes' if has_dapr else 'No'}")
        sys.exit(0)
    else:
        print(f"✗ {service_name}: {running}/{total} pods running")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python verify.py <service-name>")
        sys.exit(1)
    verify_service(sys.argv[1])
