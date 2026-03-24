#!/usr/bin/env python3
"""Run LearnFlow database migrations."""
import subprocess
import sys

MIGRATIONS = [
    'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";',
    """CREATE TABLE IF NOT EXISTS users (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        email VARCHAR(255) UNIQUE NOT NULL,
        name VARCHAR(255) NOT NULL,
        role VARCHAR(20) NOT NULL CHECK (role IN ('student', 'teacher')),
        created_at TIMESTAMP DEFAULT NOW()
    );""",
    """CREATE TABLE IF NOT EXISTS progress (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        user_id UUID REFERENCES users(id) ON DELETE CASCADE,
        module INTEGER NOT NULL CHECK (module BETWEEN 1 AND 8),
        topic VARCHAR(255) NOT NULL,
        mastery_score FLOAT DEFAULT 0.0 CHECK (mastery_score BETWEEN 0.0 AND 1.0),
        exercises_completed INTEGER DEFAULT 0,
        quiz_score FLOAT DEFAULT 0.0,
        code_quality FLOAT DEFAULT 0.0,
        streak_days INTEGER DEFAULT 0,
        updated_at TIMESTAMP DEFAULT NOW(),
        UNIQUE(user_id, module, topic)
    );""",
    """CREATE TABLE IF NOT EXISTS code_submissions (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        user_id UUID REFERENCES users(id) ON DELETE CASCADE,
        module INTEGER NOT NULL,
        code TEXT NOT NULL,
        output TEXT,
        is_correct BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT NOW()
    );""",
    """CREATE TABLE IF NOT EXISTS struggle_alerts (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        student_id UUID REFERENCES users(id) ON DELETE CASCADE,
        teacher_id UUID REFERENCES users(id),
        trigger_type VARCHAR(50) NOT NULL,
        details JSONB DEFAULT '{}',
        resolved BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT NOW()
    );""",
]


def run_migrations():
    pg_pod = subprocess.run(
        ["kubectl", "get", "pods", "-n", "postgres", "-l", "app.kubernetes.io/name=postgresql",
         "-o", "jsonpath={.items[0].metadata.name}"],
        capture_output=True, text=True,
    ).stdout.strip()

    if not pg_pod:
        print("✗ No PostgreSQL pod found")
        sys.exit(1)

    applied = 0
    for i, migration in enumerate(MIGRATIONS, 1):
        result = subprocess.run(
            ["kubectl", "exec", "-n", "postgres", pg_pod, "--",
             "psql", "-U", "learnflow", "-d", "learnflow", "-c", migration.strip()],
            capture_output=True, text=True,
        )
        if result.returncode == 0:
            applied += 1
        else:
            print(f"✗ Migration {i} failed: {result.stderr.strip()}")

    print(f"✓ {applied}/{len(MIGRATIONS)} migrations applied")

    result = subprocess.run(
        ["kubectl", "exec", "-n", "postgres", pg_pod, "--",
         "psql", "-U", "learnflow", "-d", "learnflow", "-c",
         "SELECT tablename FROM pg_tables WHERE schemaname='public';"],
        capture_output=True, text=True,
    )
    if result.returncode == 0:
        print(f"✓ Tables created successfully")


if __name__ == "__main__":
    run_migrations()
