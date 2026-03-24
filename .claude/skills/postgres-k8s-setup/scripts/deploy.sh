#!/bin/bash
set -e

echo "Deploying PostgreSQL to Kubernetes..."

helm repo add bitnami https://charts.bitnami.com/bitnami 2>/dev/null || true
helm repo update

kubectl create namespace postgres --dry-run=client -o yaml | kubectl apply -f -

helm upgrade --install postgresql bitnami/postgresql --namespace postgres \
  --set auth.database=learnflow \
  --set auth.username=learnflow \
  --set auth.password=learnflow-secret \
  --set primary.persistence.size=8Gi \
  --wait --timeout=300s

echo "✓ PostgreSQL deployed to namespace 'postgres'"
echo "  Database: learnflow | User: learnflow"
echo "  Service: postgresql.postgres.svc.cluster.local:5432"
