## Why

Sensitive credentials (`SECRET_KEY`, `DATABASE_*`, `OPENAI_API_KEY`) are currently read from a `.env` file, which risks accidental exposure through version control or container images. Migrating to AWS Secrets Manager eliminates secrets from the filesystem and enables centralized rotation in the production ECS environment.

## What Changes

- New `infrastructure/config.py` module that fetches all secrets from AWS Secrets Manager at startup and injects them into `os.environ`
- `app.py` calls `load_secrets_into_env()` as the very first action, before any other porter imports
- `DATABASE_URL` is assembled from individual SM fields (`DATABASE_HOST`, `DATABASE_PORT`, `DATABASE_USER`, `DATABASE_PASSWORD`, `DATABASE_NAME`) instead of being stored as a single string
- `boto3` added as a project dependency
- When `PORTER_SECRETS_NAME` env var is not set, the module is a no-op — local dev continues to use `.env` unchanged

## Capabilities

### New Capabilities

- `secrets-loading`: Fetches secrets from AWS Secrets Manager at application startup and makes them available as environment variables; assembles `DATABASE_URL` from individual credential fields

### Modified Capabilities

_(none — no existing spec-level behavior changes)_

## Impact

- **New file**: `source/porter/infrastructure/config.py`
- **Modified file**: `source/porter/app.py` (2 lines added at top)
- **Modified file**: `pyproject.toml` (`boto3` dependency added)
- **AWS**: ECS Task Role requires `secretsmanager:GetSecretValue` on the `porter-secrets` secret ARN; `PORTER_SECRETS_NAME=porter-secrets` env var set in the ECS task definition
- **No changes to**: `database.py`, `scraper.py`, `service.py`, or any other file
