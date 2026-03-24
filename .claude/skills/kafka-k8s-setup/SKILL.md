---
name: kafka-k8s-setup
description: Deploy Apache Kafka on Kubernetes using Helm charts
---

# Kafka Kubernetes Setup

## When to Use
- User asks to deploy Kafka or event streaming
- Setting up event-driven microservices
- LearnFlow needs async messaging infrastructure

## Instructions
1. Run deployment: `bash scripts/deploy.sh`
2. Verify status: `python scripts/verify.py`
3. Create topics: `python scripts/create_topics.py`
4. Confirm all pods Running before proceeding

## Validation
- [ ] All Kafka pods in Running state
- [ ] Can create and list test topics
- [ ] Producer/consumer test passes

See [REFERENCE.md](./REFERENCE.md) for configuration options.
