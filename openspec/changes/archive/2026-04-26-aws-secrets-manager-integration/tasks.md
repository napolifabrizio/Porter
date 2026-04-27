## 1. Dependencies

- [x] 1.1 Add `boto3` to `pyproject.toml` dependencies
- [x] 1.2 Run `poetry lock` and `poetry install` to update the lockfile

## 2. Secrets Loader Module

- [x] 2.1 Create `source/porter/infrastructure/config.py` with a `load_secrets_into_env()` function
- [x] 2.2 Implement the no-op path: if `PORTER_SECRETS_NAME` is not set, return immediately
- [x] 2.3 Implement the SM fetch path: call `boto3.client("secretsmanager").get_secret_value()` with the secret name
- [x] 2.4 Parse the JSON secret string into a dict
- [x] 2.5 Assemble `DATABASE_URL` as `postgresql://USER:PASSWORD@HOST:PORT/NAME` from the individual fields
- [x] 2.6 Inject `DATABASE_URL`, `SECRET_KEY`, and `OPENAI_API_KEY` into `os.environ`

## 3. App Entry Point

- [x] 3.1 In `source/porter/app.py`, add `from porter.infrastructure.config import load_secrets_into_env` as the first import
- [x] 3.2 Call `load_secrets_into_env()` immediately after that import, before all other porter imports

## 4. AWS Configuration

- [ ] 4.1 Grant the ECS Task Role `secretsmanager:GetSecretValue` permission scoped to the `porter-secrets` secret ARN
- [x] 4.2 Add `PORTER_SECRETS_NAME=porter-secrets` as an environment variable in the ECS task definition
- [x] 4.3 Remove any hardcoded `DATABASE_URL`, `SECRET_KEY`, `OPENAI_API_KEY` env vars from the ECS task definition (now sourced from SM)

## 5. Verification

- [ ] 5.1 Deploy and confirm `/health` returns 200
- [ ] 5.2 Confirm a product can be tracked end-to-end (scrape + DB write)
- [ ] 5.3 Confirm login returns a JWT (SECRET_KEY used correctly)
