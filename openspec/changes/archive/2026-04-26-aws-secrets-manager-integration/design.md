## Context

The Porter backend (FastAPI on ECS Fargate) currently reads `SECRET_KEY`, `DATABASE_URL`, and `OPENAI_API_KEY` from environment variables populated by a `.env` file. In production, this means secrets must be baked into the deployment environment or injected manually.

AWS Secrets Manager (`porter-secrets`) already holds all credentials as a single JSON secret with keys: `DATABASE_HOST`, `DATABASE_PORT`, `DATABASE_USER`, `DATABASE_PASSWORD`, `DATABASE_NAME`, `SECRET_KEY`, `OPENAI_API_KEY`. The goal is to have the application fetch them at startup instead of reading from `.env`.

The startup sequence matters: `service.py` calls `load_dotenv()` at module import time, and `AppService.__init__` immediately creates `Database()`, which reads `DATABASE_URL`. The SM fetch must happen before either of these.

## Goals / Non-Goals

**Goals:**
- Fetch all secrets from SM at startup when running on AWS
- Assemble `DATABASE_URL` from individual SM fields at runtime
- Preserve `.env`-based local dev workflow with zero changes
- Touch as few files as possible (single new file + 2 lines in `app.py`)

**Non-Goals:**
- Secret rotation without container restart
- Per-secret IAM granularity (all secrets in one JSON blob)
- Changing how `database.py`, `scraper.py`, or `service.py` read their config

## Decisions

### Detection: env var flag, not environment name

**Decision**: Use `PORTER_SECRETS_NAME` env var to signal SM mode. When set, fetch from SM. When absent, do nothing.

**Rationale**: Explicit over implicit. No hardcoded env names (`"production"`, `"staging"`). The ECS task definition sets `PORTER_SECRETS_NAME=porter-secrets`; local dev leaves it unset.

**Alternative considered**: Auto-detect AWS environment via `boto3.utils` or metadata endpoint. Rejected — adds latency and complexity; fails noisily in non-AWS cloud environments.

### Injection strategy: populate `os.environ`, not a Config object

**Decision**: `load_secrets_into_env()` injects values into `os.environ` in-place, so all existing reads (`os.environ["SECRET_KEY"]`, `os.environ["DATABASE_URL"]`, `ChatOpenAI()`) continue unchanged.

**Rationale**: Zero changes to `database.py`, `scraper.py`, `service.py`. `load_dotenv()` in `service.py` won't override vars already set in `os.environ` (default behavior of python-dotenv).

**Alternative considered**: A `Config` dataclass passed through constructors. Rejected — requires touching every call site; more invasive than the problem warrants.

### One JSON secret, one API call

**Decision**: All 7 secrets live in a single `porter-secrets` JSON blob. One `GetSecretValue` call at startup fetches everything.

**Rationale**: Simpler IAM rule (one ARN), fewer API calls, one rotation point. Fine-grained per-secret access control is not needed at Porter's scale.

### Placement: first lines of `app.py`

**Decision**: `load_secrets_into_env()` is called at the very top of `app.py`, before any porter imports.

**Rationale**: Python executes module-level code on import. `from porter.application.service import AppService` triggers `load_dotenv()` and eventually `Database()`. The SM fetch must precede this. Placing it in `app.py` before other imports is the minimal surgical fix.

## Risks / Trade-offs

- **SM unavailability at startup** → App fails to start; ECS health check fails and task restarts. Mitigation: SM is a regional AWS service with high availability; treat startup failure as a deployment issue, not a runtime concern.
- **boto3 cold-start latency** → `GetSecretValue` adds ~50–200ms to container startup. Acceptable since this is a one-time cost, not per-request.
- **Secrets still land in `os.environ`** → Any code with access to the process can read them. This is equivalent to the `.env` approach but secrets never touch disk. Mitigation: restrict ECS task permissions and avoid logging env vars.
- **Local dev needs AWS credentials if `PORTER_SECRETS_NAME` is accidentally set** → Mitigation: document that local dev must NOT set `PORTER_SECRETS_NAME`.

## Migration Plan

1. Add `boto3` to `pyproject.toml` and rebuild the Docker image
2. Create `infrastructure/config.py` with `load_secrets_into_env()`
3. Add the two-line call at the top of `app.py`
4. Grant the ECS Task Role `secretsmanager:GetSecretValue` on the `porter-secrets` ARN
5. Add `PORTER_SECRETS_NAME=porter-secrets` to the ECS task definition environment
6. Deploy; verify `/health` returns 200
7. Remove `DATABASE_URL`, `SECRET_KEY`, `OPENAI_API_KEY` from any ECS task definition environment vars (they're now sourced from SM)

**Rollback**: Remove `PORTER_SECRETS_NAME` from task definition → app falls back to direct `os.environ` reads → re-add the individual env vars to task definition.
