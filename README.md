# DevOps Demo API — Containerized CI/CD Pipeline

A small Flask API used as the foundation for a full DevOps pipeline: containerization,
automated testing, image vulnerability scanning, and continuous delivery via GitHub Actions.

## What this project demonstrates

- **Multi-stage Docker builds** — separates build dependencies from the runtime image,
  keeping the final image small.
- **Non-root container execution** — the app runs as an unprivileged `appuser`, not root.
- **CI/CD with GitHub Actions** — every push/PR is linted, tested, built, and scanned
  before anything reaches the registry.
- **Vulnerability scanning** — Trivy scans the built image for known CVEs on every run.
- **Local multi-service dev environment** — `docker-compose` runs the API alongside Postgres.

## Architecture

```
Developer -> GitHub PR -> GitHub Actions
                              |-> Lint (ruff)
                              |-> Test (pytest)
                              |-> Build Docker image
                              |-> Scan image (Trivy)
                              |-> Push to GHCR (on main only)
                                        |
                                        v
                              Deployed container (Render/Fly.io)
```

## Endpoints

| Method | Path      | Description                |
|--------|-----------|-----------------------------|
| GET    | `/`       | Welcome message             |
| GET    | `/health` | Health check for probes/LB  |
| GET    | `/items`  | List items                  |
| POST   | `/items`  | Add an item (`{"name": ...}`)|

## Running locally

```bash
# With Docker Compose (app + Postgres)
docker-compose up --build

# Or just the app
pip install -r requirements.txt
python app.py
```

## Running tests

```bash
pytest -v
```

## Why these choices

- **Multi-stage build**: cuts the final image size significantly by discarding build-only
  tools and caches, and reduces the attack surface.
- **Pinned base image tags**: `python:3.12-slim` instead of `latest`, so builds are
  reproducible and don't silently break.
- **SHA-tagged images**: every image pushed to GHCR is tagged with the commit SHA,
  so you always know exactly which code is running in production.
- **Trivy scanning in CI**: catches known vulnerabilities before they ship, not after.

## Next steps (future projects)

- Add Kubernetes manifests / Helm chart for deployment
- Add Terraform for provisioning infrastructure
- Add Prometheus/Grafana for monitoring
- Enforce branch protection so `main` requires a passing pipeline
