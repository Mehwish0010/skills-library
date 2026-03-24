#!/bin/bash
set -e

FRONTEND_DIR="${1:-services/frontend}"

echo "Deploying LearnFlow frontend to Kubernetes..."
kubectl apply -f "$FRONTEND_DIR/k8s/"
echo "✓ Frontend deployed"
kubectl get pods -l app=learnflow-frontend
