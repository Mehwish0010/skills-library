#!/bin/bash
set -e

DOCS_DIR="${1:-docs-site}"

echo "Deploying LearnFlow documentation to Kubernetes..."
kubectl apply -f "$DOCS_DIR/k8s/"
echo "✓ Documentation site deployed"
kubectl get pods -l app=learnflow-docs
