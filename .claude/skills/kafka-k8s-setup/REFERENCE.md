# Kafka on Kubernetes Reference

## Architecture
- Uses Bitnami Helm chart for Kafka deployment
- Runs in dedicated `kafka` namespace
- Single-node setup for development (scalable for production)

## Configuration Options
| Parameter | Default | Description |
|-----------|---------|-------------|
| replicaCount | 1 | Number of Kafka brokers |
| controller.replicaCount | 1 | Number of KRaft controllers |
| persistence.size | 8Gi | Storage per broker |
| listeners.client.protocol | PLAINTEXT | Client protocol |

## LearnFlow Topics
| Topic | Purpose | Partitions |
|-------|---------|------------|
| learning.events | Student learning activities | 3 |
| code.submissions | Code execution requests | 3 |
| exercise.events | Exercise creation/completion | 3 |
| struggle.alerts | Struggle detection notifications | 1 |
| progress.updates | Mastery score changes | 3 |

## Troubleshooting
- **Pods Pending**: Check `kubectl describe pod` for resource issues
- **CrashLoopBackOff**: Check logs with `kubectl logs <pod> -n kafka`
- **Connection refused**: Verify service with `kubectl get svc -n kafka`

## Scaling for Production
```yaml
replicaCount: 3
controller:
  replicaCount: 3
persistence:
  size: 50Gi
resources:
  requests:
    memory: 2Gi
    cpu: 500m
```
