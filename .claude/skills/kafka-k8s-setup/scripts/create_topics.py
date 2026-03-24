#!/usr/bin/env python3
"""Create LearnFlow Kafka topics."""
import subprocess
import sys

TOPICS = [
    {"name": "learning.events", "partitions": 3},
    {"name": "code.submissions", "partitions": 3},
    {"name": "exercise.events", "partitions": 3},
    {"name": "struggle.alerts", "partitions": 1},
    {"name": "progress.updates", "partitions": 3},
]


def create_topics():
    kafka_pod = subprocess.run(
        ["kubectl", "get", "pods", "-n", "kafka", "-l", "app.kubernetes.io/component=kafka",
         "-o", "jsonpath={.items[0].metadata.name}"],
        capture_output=True, text=True,
    ).stdout.strip()

    if not kafka_pod:
        print("✗ No Kafka pod found")
        sys.exit(1)

    created = 0
    for topic in TOPICS:
        result = subprocess.run(
            ["kubectl", "exec", "-n", "kafka", kafka_pod, "--",
             "kafka-topics.sh", "--create",
             "--bootstrap-server", "localhost:9092",
             "--topic", topic["name"],
             "--partitions", str(topic["partitions"]),
             "--replication-factor", "1",
             "--if-not-exists"],
            capture_output=True, text=True,
        )
        if result.returncode == 0:
            created += 1

    print(f"✓ {created}/{len(TOPICS)} topics created")

    result = subprocess.run(
        ["kubectl", "exec", "-n", "kafka", kafka_pod, "--",
         "kafka-topics.sh", "--list", "--bootstrap-server", "localhost:9092"],
        capture_output=True, text=True,
    )
    if result.returncode == 0:
        topics = [t for t in result.stdout.strip().split("\n") if t]
        print(f"✓ Active topics: {', '.join(topics)}")


if __name__ == "__main__":
    create_topics()
