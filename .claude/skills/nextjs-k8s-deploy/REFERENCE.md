# Next.js Kubernetes Deployment Reference

## Tech Stack
- Next.js 14+ (App Router)
- TypeScript
- Monaco Editor (@monaco-editor/react)
- Tailwind CSS
- Better Auth for authentication

## Page Structure
| Route | Component | Description |
|-------|-----------|-------------|
| / | Landing | Welcome page with login |
| /dashboard | StudentDashboard | Student progress overview |
| /chat | ChatInterface | AI tutor conversation |
| /editor | CodeEditor | Monaco editor + execution |
| /quiz | QuizView | Interactive quizzes |
| /teacher | TeacherDashboard | Class monitoring |
| /teacher/exercises | ExerciseManager | Create/assign exercises |

## Dockerfile Template
```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public
EXPOSE 3000
CMD ["node", "server.js"]
```

## K8s Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: learnflow-frontend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: learnflow-frontend
  template:
    metadata:
      labels:
        app: learnflow-frontend
    spec:
      containers:
        - name: frontend
          image: learnflow/frontend:latest
          ports:
            - containerPort: 3000
          env:
            - name: NEXT_PUBLIC_API_URL
              value: "http://kong-proxy.kong.svc.cluster.local"
```

## Environment Variables
| Variable | Description |
|----------|-------------|
| NEXT_PUBLIC_API_URL | Backend API gateway URL |
| NEXTAUTH_SECRET | Auth secret key |
| NEXTAUTH_URL | App URL for auth callbacks |
