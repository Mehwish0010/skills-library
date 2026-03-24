#!/bin/bash
set -e

SERVICE_NAME=${1:?"Usage: build.sh <service-name>"}
SERVICE_DIR="services/${SERVICE_NAME}"

if [ ! -d "$SERVICE_DIR" ]; then
    echo "✗ Service directory not found: $SERVICE_DIR"
    exit 1
fi

echo "Building Docker image for ${SERVICE_NAME}..."
eval $(minikube docker-env 2>/dev/null) || true
docker build -t "learnflow/${SERVICE_NAME}:latest" "$SERVICE_DIR"
echo "✓ Built learnflow/${SERVICE_NAME}:latest"
