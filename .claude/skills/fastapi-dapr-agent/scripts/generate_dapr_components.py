#!/usr/bin/env python3
"""Generate Dapr component configurations for LearnFlow."""
import os
import sys

COMPONENTS = {
    "pubsub.yaml": """apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: learnflow-pubsub
  namespace: default
spec:
  type: pubsub.kafka
  version: v1
  metadata:
    - name: brokers
      value: "kafka.kafka.svc.cluster.local:9092"
    - name: authType
      value: "none"
""",
    "statestore.yaml": """apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: learnflow-statestore
  namespace: default
spec:
  type: state.postgresql
  version: v1
  metadata:
    - name: connectionString
      value: "host=postgresql.postgres.svc.cluster.local user=learnflow password=learnflow-secret dbname=learnflow sslmode=disable"
""",
}


def generate_components(output_dir="dapr/components"):
    os.makedirs(output_dir, exist_ok=True)
    for filename, content in COMPONENTS.items():
        with open(os.path.join(output_dir, filename), "w") as f:
            f.write(content)
    print(f"✓ Generated {len(COMPONENTS)} Dapr components in {output_dir}")


if __name__ == "__main__":
    output = sys.argv[1] if len(sys.argv) > 1 else "dapr/components"
    generate_components(output)
