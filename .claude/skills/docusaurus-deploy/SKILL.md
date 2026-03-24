---
name: docusaurus-deploy
description: Deploy Docusaurus documentation site for LearnFlow on Kubernetes
---

# Docusaurus Documentation Deployment

## When to Use
- Setting up project documentation site
- Deploying Docusaurus to Kubernetes
- Auto-generating API documentation

## Instructions
1. Scaffold Docusaurus site: `python scripts/scaffold.py`
2. Build static site: `bash scripts/build.sh`
3. Deploy to K8s: `bash scripts/deploy.sh`
4. Verify: `python scripts/verify.py`

## Documentation Structure
- Getting Started guide
- Architecture overview
- Skills reference
- API documentation
- Deployment guide

## Validation
- [ ] Docusaurus builds without errors
- [ ] Docker image created
- [ ] Pods running on K8s
- [ ] Documentation site accessible

See [REFERENCE.md](./REFERENCE.md) for configuration.
