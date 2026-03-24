#!/bin/bash
set -e

echo "Deploying Kafka to Kubernetes..."

helm repo add bitnami https://charts.bitnami.com/bitnami 2>/dev/null || true
helm repo update

kubectl create namespace kafka --dry-run=client -o yaml | kubectl apply -f -

helm upgrade --install kafka bitnami/kafka --namespace kafka \
  --set replicaCount=1 \
  --set controller.replicaCount=1 \
  --set listeners.client.protocol=PLAINTEXT \
  --set listeners.interbroker.protocol=PLAINTEXT \
  --set persistence.size=8Gi \
  --wait --timeout=300s

echo "✓ Kafka deployed to namespace 'kafka'"
