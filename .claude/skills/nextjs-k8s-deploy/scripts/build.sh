#!/bin/bash
set -e

FRONTEND_DIR="${1:-services/frontend}"

echo "Building LearnFlow frontend Docker image..."
eval $(minikube docker-env 2>/dev/null) || true
docker build -t learnflow/frontend:latest "$FRONTEND_DIR"
echo "✓ Built learnflow/frontend:latest"
