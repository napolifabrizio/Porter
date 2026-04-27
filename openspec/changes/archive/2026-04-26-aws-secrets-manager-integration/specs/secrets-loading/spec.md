## ADDED Requirements

### Requirement: Fetch secrets from AWS Secrets Manager at startup
When `PORTER_SECRETS_NAME` is set in the environment, the application SHALL fetch the named secret from AWS Secrets Manager and inject all credential values into `os.environ` before any other application module reads them.

#### Scenario: SM fetch succeeds
- **WHEN** `PORTER_SECRETS_NAME` is set and the secret exists in AWS Secrets Manager
- **THEN** `os.environ` SHALL contain `SECRET_KEY`, `DATABASE_URL`, `OPENAI_API_KEY` with values derived from the secret

#### Scenario: PORTER_SECRETS_NAME is not set
- **WHEN** `PORTER_SECRETS_NAME` is absent from the environment
- **THEN** `load_secrets_into_env()` SHALL return without making any AWS API calls and `os.environ` SHALL remain unchanged

#### Scenario: SM fetch fails
- **WHEN** `PORTER_SECRETS_NAME` is set but the AWS call fails (permissions error, network, secret not found)
- **THEN** the application SHALL raise an exception and fail to start

### Requirement: Assemble DATABASE_URL from individual credential fields
The application SHALL construct a valid PostgreSQL connection URL from the individual secret fields rather than storing the full URL as a secret.

#### Scenario: All database fields present
- **WHEN** the secret contains `DATABASE_HOST`, `DATABASE_PORT`, `DATABASE_USER`, `DATABASE_PASSWORD`, and `DATABASE_NAME`
- **THEN** `os.environ["DATABASE_URL"]` SHALL be set to `postgresql://USER:PASSWORD@HOST:PORT/NAME`

#### Scenario: A required database field is missing
- **WHEN** one or more of `DATABASE_HOST`, `DATABASE_PORT`, `DATABASE_USER`, `DATABASE_PASSWORD`, `DATABASE_NAME` is absent from the secret
- **THEN** the application SHALL raise a `KeyError` and fail to start

### Requirement: Local development is unaffected
The application SHALL continue to support `.env`-based configuration when `PORTER_SECRETS_NAME` is not set, with no code changes required in local dev workflow.

#### Scenario: Local dev with .env file
- **WHEN** `PORTER_SECRETS_NAME` is not set and a `.env` file is present
- **THEN** `load_dotenv()` in `service.py` SHALL populate `os.environ` as before and the application SHALL start normally

### Requirement: SM-sourced values take precedence over .env
When running with `PORTER_SECRETS_NAME` set, SM values SHALL not be overridden by `load_dotenv()`.

#### Scenario: .env file also present in production
- **WHEN** `PORTER_SECRETS_NAME` is set and a `.env` file also exists
- **THEN** SM-injected values SHALL remain in `os.environ` unchanged after `load_dotenv()` runs (python-dotenv does not override existing env vars by default)
