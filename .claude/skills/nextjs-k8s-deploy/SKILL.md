---
name: nextjs-k8s-deploy
description: Deploy Next.js frontend application with Monaco editor on Kubernetes
---

# Next.js Kubernetes Deployment

## When to Use
- Deploying the LearnFlow frontend
- Setting up Next.js applications on Kubernetes
- Building UI with Monaco code editor

## Instructions
1. Scaffold the Next.js app: `python scripts/scaffold.py`
2. Build Docker image: `bash scripts/build.sh`
3. Deploy to K8s: `bash scripts/deploy.sh`
4. Verify: `python scripts/verify.py`

## LearnFlow Frontend Features
- Student dashboard with progress tracking
- Chat interface for AI tutoring agents
- Monaco code editor for writing/running Python
- Quiz and exercise components
- Teacher dashboard with class monitoring

## Validation
- [ ] Next.js app builds successfully
- [ ] Docker image created
- [ ] Pods running on K8s
- [ ] Frontend accessible via service URL

See [REFERENCE.md](./REFERENCE.md) for component details.
