# Docusaurus Deployment Reference

## Structure
```
docs-site/
├── docs/
│   ├── intro.md
│   ├── getting-started/
│   ├── architecture/
│   ├── skills/
│   └── api/
├── src/pages/
├── static/
├── docusaurus.config.js
├── Dockerfile
└── k8s/
    ├── deployment.yaml
    └── service.yaml
```

## Dockerfile
```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
EXPOSE 80
```

## K8s Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: learnflow-docs
spec:
  replicas: 1
  selector:
    matchLabels:
      app: learnflow-docs
  template:
    metadata:
      labels:
        app: learnflow-docs
    spec:
      containers:
        - name: docs
          image: learnflow/docs:latest
          ports:
            - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: learnflow-docs
spec:
  selector:
    app: learnflow-docs
  ports:
    - port: 80
      targetPort: 80
  type: ClusterIP
```
