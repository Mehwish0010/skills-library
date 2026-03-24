#!/bin/bash
set -e

DOCS_DIR="${1:-docs-site}"

echo "Building Docusaurus documentation site..."
eval $(minikube docker-env 2>/dev/null) || true
docker build -t learnflow/docs:latest "$DOCS_DIR"
echo "✓ Built learnflow/docs:latest"
