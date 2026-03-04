# Developer Guide

## Stack

- Backend: FastAPI, SQLAlchemy async, FastAPI Users, Celery
- Frontend: React + TypeScript + Vite
- Data: PostgreSQL + pgvector
- Queue: Redis

## Prerequisites

- Python 3.11+
- Node.js 18+
- Docker + Docker Compose (recommended)

## Run with Docker (recommended)

```bash
docker compose up --build -d
```

## Run backend locally

```bash
cd backend
python -m venv .venv
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Run frontend locally

```bash
cd frontend
npm install
npm run dev
```

## Auth/API contracts

- Login: `POST /api/v1/auth/jwt/login`
- Register: `POST /api/v1/auth/register`
- Forgot password: `POST /api/v1/auth/forgot-password`
- Reset password: `POST /api/v1/auth/reset-password`
- Current user: `GET /api/v1/users/me`
- Dashboard stats: `GET /api/v1/users/me/dashboard`
- Analyze: `POST /api/v1/analyze`
- Batch results: `GET /api/v1/batches/{batch_id}/results`
- Admin users: `/api/admin/users`

## Environment variables

Use `backend/.env.docker.example` as baseline.

Required for safe usage:

- `SECRET_KEY`
- `ADMIN_EMAIL`
- `ADMIN_PASSWORD`

Optional:

- `CREATE_SAMPLE_USERS=true` for demo environments only
- `OPENAI_API_KEY` and/or `TOGETHER_API_KEY`

## Quality checks

```bash
# Backend syntax check without writing pycache
python - <<'PY'
import pathlib
for p in pathlib.Path('backend/app').rglob('*.py'):
    compile(p.read_text(), str(p), 'exec')
print('ok')
PY

# Frontend
cd frontend && npm run build
cd frontend && npm run lint
```

## Notes

- The backend now supports both canonical and v1 aliases for auth/user routes.
- Sample user seeding is opt-in to avoid insecure default credentials in normal setups.
