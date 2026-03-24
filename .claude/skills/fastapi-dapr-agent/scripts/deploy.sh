#!/bin/bash
set -e

SERVICE_NAME=${1:?"Usage: deploy.sh <service-name>"}
SERVICE_DIR="services/${SERVICE_NAME}"

if [ ! -d "$SERVICE_DIR/k8s" ]; then
    echo "✗ K8s manifests not found: $SERVICE_DIR/k8s"
    exit 1
fi

echo "Deploying ${SERVICE_NAME} to Kubernetes..."
kubectl apply -f "$SERVICE_DIR/k8s/"
echo "✓ Deployed ${SERVICE_NAME}"
kubectl get pods -l app="${SERVICE_NAME}"
