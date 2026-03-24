---
name: fastapi-dapr-agent
description: Create FastAPI microservices with Dapr sidecar and AI agent capabilities
---

# FastAPI + Dapr Agent Service

## When to Use
- Creating backend microservices for LearnFlow
- Setting up AI-powered tutoring agents
- Building services with Dapr pub/sub or state management

## Instructions
1. Generate service scaffold: `python scripts/scaffold_service.py <service-name>`
2. Generate Dapr components: `python scripts/generate_dapr_components.py`
3. Build Docker image: `bash scripts/build.sh <service-name>`
4. Deploy to K8s: `bash scripts/deploy.sh <service-name>`
5. Verify: `python scripts/verify.py <service-name>`

## LearnFlow Agents
- **triage-agent**: Routes queries to specialist agents
- **concepts-agent**: Explains Python concepts with examples
- **code-review-agent**: Analyzes code for correctness and style
- **debug-agent**: Parses errors and provides debugging guidance
- **exercise-agent**: Generates and auto-grades coding challenges
- **progress-agent**: Tracks mastery scores and progress summaries

## Validation
- [ ] Service starts and responds to health check
- [ ] Dapr sidecar is running
- [ ] Can publish/subscribe to Kafka topics
- [ ] AI agent responds to test prompts

See [REFERENCE.md](./REFERENCE.md) for service templates and Dapr patterns.
