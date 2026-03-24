# PostgreSQL on Kubernetes Reference

## Architecture
- Uses Bitnami Helm chart
- Runs in `postgres` namespace
- Persistent storage via PVC

## LearnFlow Database Schema

### users
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| email | VARCHAR(255) | User email |
| name | VARCHAR(255) | Display name |
| role | ENUM | 'student' or 'teacher' |
| created_at | TIMESTAMP | Account creation |

### progress
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| user_id | UUID | FK to users |
| module | INTEGER | Module number (1-8) |
| topic | VARCHAR(255) | Topic name |
| mastery_score | FLOAT | 0.0 to 1.0 |
| exercises_completed | INTEGER | Count |
| quiz_score | FLOAT | Average quiz score |
| code_quality | FLOAT | Average code quality |
| streak_days | INTEGER | Consecutive days |
| updated_at | TIMESTAMP | Last update |

### code_submissions
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| user_id | UUID | FK to users |
| module | INTEGER | Module number |
| code | TEXT | Submitted code |
| output | TEXT | Execution output |
| is_correct | BOOLEAN | Pass/fail |
| created_at | TIMESTAMP | Submission time |

### struggle_alerts
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| student_id | UUID | FK to users |
| teacher_id | UUID | FK to users |
| trigger_type | VARCHAR(50) | What triggered alert |
| details | JSONB | Context data |
| resolved | BOOLEAN | Alert resolved |
| created_at | TIMESTAMP | Alert time |

## Connection Details
- Host: `postgresql.postgres.svc.cluster.local`
- Port: `5432`
- Database: `learnflow`
- Default user: `learnflow`
