# FastAPI + Dapr Agent Reference

## Service Template Structure
```
services/<service-name>/
├── main.py              # FastAPI application
├── agent.py             # AI agent logic (OpenAI SDK)
├── models.py            # Pydantic models
├── requirements.txt     # Dependencies
├── Dockerfile           # Container image
├── dapr/components/     # Dapr component configs
└── k8s/
    ├── deployment.yaml  # K8s deployment
    └── service.yaml     # K8s service
```

## Agent Architecture

### Triage Agent
- Routes to: concepts, code-review, debug, exercise, progress
- Keywords: "explain" → concepts, "error/bug" → debug, "review" → code-review

### Concepts Agent
- Explains Python topics from Module 1-8
- Adapts depth to student mastery level

### Code Review Agent
- Checks: correctness, PEP 8 style, efficiency, readability

### Debug Agent
- Parses Python error messages, provides hints before solutions (Socratic method)

### Exercise Agent
- Generates exercises based on module/topic, auto-grades submissions

### Progress Agent
- Mastery: exercises(40%) + quiz(30%) + code_quality(20%) + streak(10%)
- Levels: 0-40% Beginner, 41-70% Learning, 71-90% Proficient, 91-100% Mastered

## Dapr Pub/Sub Component (Kafka)
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: learnflow-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
    - name: brokers
      value: "kafka.kafka.svc.cluster.local:9092"
    - name: authType
      value: "none"
```

## Dapr State Store (PostgreSQL)
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: learnflow-statestore
spec:
  type: state.postgresql
  version: v1
  metadata:
    - name: connectionString
      value: "host=postgresql.postgres.svc.cluster.local user=learnflow password=learnflow-secret dbname=learnflow sslmode=disable"
```

## Struggle Detection Rules
- Same error type 3+ times
- Stuck on exercise > 10 minutes
- Quiz score < 50%
- Student says "I don't understand" / "I'm stuck"
- 5+ failed code executions in a row
