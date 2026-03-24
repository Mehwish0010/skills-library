---
name: postgres-k8s-setup
description: Deploy PostgreSQL on Kubernetes and run database migrations
---

# PostgreSQL Kubernetes Setup

## When to Use
- User asks to deploy PostgreSQL or a database
- Setting up persistent storage for LearnFlow
- Running database migrations

## Instructions
1. Deploy PostgreSQL: `bash scripts/deploy.sh`
2. Verify deployment: `python scripts/verify.py`
3. Run migrations: `python scripts/migrate.py`
4. Confirm database is accessible

## Validation
- [ ] PostgreSQL pod in Running state
- [ ] Can connect to database
- [ ] All migrations applied successfully
- [ ] LearnFlow tables created

See [REFERENCE.md](./REFERENCE.md) for schema details.
