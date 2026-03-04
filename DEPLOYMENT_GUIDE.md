# Deployment Guide

## 1. Recommended: Docker Compose

### Prerequisites

- Docker Compose v2+
- 8 GB RAM minimum (16 GB recommended for heavy NLP workloads)

### Setup

1. Copy env file:

macOS/Linux:

```bash
cp backend/.env.docker.example backend/.env.docker
```

Windows PowerShell:

```powershell
Copy-Item backend/.env.docker.example backend/.env.docker
```

2. Edit `backend/.env.docker`:

- Set `SECRET_KEY` to a strong random value.
- Set `ADMIN_EMAIL` and `ADMIN_PASSWORD`.
- Keep `CREATE_SAMPLE_USERS=false` unless you are in a demo environment.

3. Start services:

```bash
docker compose up --build -d
```

4. Validate:

```bash
curl -sS http://localhost:8000/health
```

## 2. Service endpoints

- Frontend: `http://localhost`
- API docs: `http://localhost:8000/docs`
- MinIO console: `http://localhost:9001`

## 3. Production checklist

- Set `ENVIRONMENT=production`.
- Use a strong `SECRET_KEY` (required in production mode).
- Rotate DB, MinIO, and admin credentials.
- Terminate TLS at reverse proxy/load balancer.
- Restrict exposed ports.
- Configure backups for PostgreSQL and object storage.
- Monitor API and worker logs.

## 4. Scaling

- Scale Celery workers first for throughput.
- Scale API replicas behind a reverse proxy.
- Increase PostgreSQL resources as embeddings and comparisons grow.

## 5. Common operations

```bash
# Restart
docker compose restart

# Stop
docker compose down

# Stop and remove volumes (destructive)
docker compose down -v

# Logs
docker compose logs -f api
docker compose logs -f celery-worker
```
