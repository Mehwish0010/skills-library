#!/usr/bin/env python3
"""Scaffold a new FastAPI + Dapr agent microservice."""
import os
import sys

AGENT_PROMPTS = {
    "triage-agent": "You are the LearnFlow Triage Agent. Analyze student queries and route them to the appropriate specialist. Route 'explain' queries to concepts-agent, 'error/bug' queries to debug-agent, code review requests to code-review-agent, exercise requests to exercise-agent, and progress queries to progress-agent.",
    "concepts-agent": "You are the LearnFlow Concepts Agent. Explain Python programming concepts clearly with code examples. Adapt your explanation depth based on the student's mastery level. Cover modules: Basics, Control Flow, Data Structures, Functions, OOP, Files, Errors, Libraries.",
    "code-review-agent": "You are the LearnFlow Code Review Agent. Analyze Python code for correctness, PEP 8 style compliance, efficiency, and readability. Provide structured line-by-line feedback with specific improvement suggestions.",
    "debug-agent": "You are the LearnFlow Debug Agent. Parse Python error messages, identify root causes, and guide students using the Socratic method - provide hints before full solutions. Help students learn to debug independently.",
    "exercise-agent": "You are the LearnFlow Exercise Agent. Generate Python coding exercises appropriate for the student's current module and mastery level. Auto-grade submissions and provide detailed feedback on solutions.",
    "progress-agent": "You are the LearnFlow Progress Agent. Track and summarize student mastery scores. Calculate mastery using: exercises(40%) + quiz(30%) + code_quality(20%) + streak(10%). Levels: 0-40% Beginner, 41-70% Learning, 71-90% Proficient, 91-100% Mastered.",
}


def scaffold(service_name):
    base_path = os.path.join("services", service_name)
    os.makedirs(base_path, exist_ok=True)
    os.makedirs(os.path.join(base_path, "dapr", "components"), exist_ok=True)
    os.makedirs(os.path.join(base_path, "k8s"), exist_ok=True)

    title = service_name.replace("-", " ").title()
    system_prompt = AGENT_PROMPTS.get(service_name, f"You are the LearnFlow {title}.")

    # main.py
    with open(os.path.join(base_path, "main.py"), "w") as f:
        f.write(f'''"""LearnFlow {title} Service."""
from fastapi import FastAPI
from pydantic import BaseModel
from agent import Agent
import httpx
import os

app = FastAPI(title="{title}", version="1.0.0")
agent = Agent()

DAPR_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
PUBSUB_NAME = "learnflow-pubsub"


class ChatRequest(BaseModel):
    user_id: str
    message: str
    context: dict = {{}}


class ChatResponse(BaseModel):
    response: str
    agent: str = "{service_name}"
    metadata: dict = {{}}


@app.get("/health")
async def health():
    return {{"status": "healthy", "service": "{service_name}"}}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    result = await agent.process(request.message, request.context)

    async with httpx.AsyncClient() as client:
        await client.post(
            f"http://localhost:{{DAPR_PORT}}/v1.0/publish/{{PUBSUB_NAME}}/learning.events",
            json={{"user_id": request.user_id, "agent": "{service_name}", "action": "chat"}},
        )

    return ChatResponse(response=result["response"], metadata=result.get("metadata", {{}}))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
''')

    # agent.py
    with open(os.path.join(base_path, "agent.py"), "w") as f:
        f.write(f'''"""AI Agent for {title}."""
from openai import OpenAI
import os


class Agent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))
        self.model = os.getenv("AI_MODEL", "gpt-4o-mini")
        self.system_prompt = """{system_prompt}"""

    async def process(self, message: str, context: dict = {{}}) -> dict:
        messages = [
            {{"role": "system", "content": self.system_prompt}},
            {{"role": "user", "content": message}},
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=1000,
        )

        return {{
            "response": response.choices[0].message.content,
            "metadata": {{"model": self.model, "tokens": response.usage.total_tokens}},
        }}
''')

    # models.py
    with open(os.path.join(base_path, "models.py"), "w") as f:
        f.write(f'''"""Pydantic models for {title}."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserContext(BaseModel):
    user_id: str
    role: str = "student"
    current_module: int = 1
    mastery_level: float = 0.0


class AgentMessage(BaseModel):
    content: str
    agent: str
    timestamp: Optional[datetime] = None
    metadata: dict = {{}}
''')

    # requirements.txt
    with open(os.path.join(base_path, "requirements.txt"), "w") as f:
        f.write("fastapi==0.115.0\nuvicorn==0.30.0\nhttpx==0.27.0\nopenai==1.50.0\npydantic==2.9.0\n")

    # Dockerfile
    with open(os.path.join(base_path, "Dockerfile"), "w") as f:
        f.write(f"""FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
""")

    # K8s deployment
    with open(os.path.join(base_path, "k8s", "deployment.yaml"), "w") as f:
        f.write(f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {service_name}
  labels:
    app: {service_name}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {service_name}
  template:
    metadata:
      labels:
        app: {service_name}
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "{service_name}"
        dapr.io/app-port: "8000"
    spec:
      containers:
        - name: {service_name}
          image: learnflow/{service_name}:latest
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8000
          env:
            - name: OPENAI_API_KEY
              valueFrom:
                secretKeyRef:
                  name: openai-secret
                  key: api-key
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 10
""")

    # K8s service
    with open(os.path.join(base_path, "k8s", "service.yaml"), "w") as f:
        f.write(f"""apiVersion: v1
kind: Service
metadata:
  name: {service_name}
spec:
  selector:
    app: {service_name}
  ports:
    - port: 80
      targetPort: 8000
  type: ClusterIP
""")

    print(f"[OK] Scaffolded {service_name} at {base_path}")
    print(f"  Files: main.py, agent.py, models.py, requirements.txt, Dockerfile")
    print(f"  K8s: deployment.yaml, service.yaml")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scaffold_service.py <service-name>")
        print("Available: triage-agent, concepts-agent, code-review-agent, debug-agent, exercise-agent, progress-agent")
        sys.exit(1)
    scaffold(sys.argv[1])
