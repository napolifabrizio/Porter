## Context

Porter is being deployed to AWS and requires a minimal access control mechanism. The app uses Streamlit (single-page, session-based) with SQLite for persistence. There is no existing auth layer. The goal is the simplest possible solution that keeps the app private without introducing user management complexity.

## Goals / Non-Goals

**Goals:**
- Block all app content behind a password entry screen on every new session
- Store the password as a bcrypt hash in the SQLite database
- Seed the hash from an `APP_PASSWORD` environment variable on first boot
- Keep the implementation self-contained with minimal new code

**Non-Goals:**
- Multi-user authentication or user accounts
- Persistent login across sessions (cookies, JWT, etc.)
- A logout button
- Password change UI within the app
- Rate limiting or brute-force protection

## Decisions

### D1: Session state for auth, not cookies
Streamlit's `st.session_state` is used to track authentication. When the session ends (tab close, refresh), the user must re-authenticate.

**Why over cookies/tokens**: Streamlit does not natively support cookies without third-party components. For a personal app, re-entering the password per session is acceptable and keeps the implementation dependency-free.

### D2: bcrypt hash stored in SQLite `app_config` table (key-value)
A new `app_config` table stores arbitrary config keys. The password hash is stored under key `password_hash`.

**Why over env var hash**: Storing the hash in the DB separates the secret (plaintext `APP_PASSWORD`) from the derived credential. The env var is only needed on first boot; after that it is not read.

**Why `app_config` over a dedicated `passwords` table**: The app has one password. A generic key-value config table is more future-proof (can store other config) without over-engineering.

**Schema:**
```sql
CREATE TABLE IF NOT EXISTS app_config (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
)
```

### D3: First-boot seeding from `APP_PASSWORD` env var
On `init_db()`, if `app_config` has no `password_hash` row and `APP_PASSWORD` is set in the environment, the app hashes the password and stores it. Subsequent boots skip seeding.

**Why not a setup screen**: An in-app setup screen on first boot is harder to secure (anyone who hits the URL first can set the password). Env var seeding is standard practice for containerized deployments.

### D4: Auth logic in `infrastructure/auth.py`
bcrypt operations (hash, verify, seed) live in a dedicated infrastructure module rather than inline in the UI.

**Why**: Keeps `ui/app.py` clean; auth logic is testable in isolation.

### D5: Lock screen uses `st.stop()`
At the very top of `app.py`, before any service calls or rendering, an auth check runs. If not authenticated, the lock screen is rendered and `st.stop()` is called — no app content is processed.

**Why**: `st.stop()` is the idiomatic Streamlit pattern for conditional rendering. It guarantees the rest of the file never executes.

## Risks / Trade-offs

| Risk | Mitigation |
|---|---|
| `APP_PASSWORD` visible in AWS env logs | Use AWS Secrets Manager or ECS secret injection; the plaintext is only needed on first boot |
| bcrypt hash in SQLite is not encrypted at rest | Acceptable for a personal app; the hash is not the plaintext password |
| No brute-force protection | Acceptable for a personal app; bcrypt cost factor slows attacks naturally |
| Streamlit session state can be reset by refresh | Known and accepted; re-authentication is the intended behavior |

## Migration Plan

1. Add `bcrypt` to `pyproject.toml` and run `poetry install`
2. Set `APP_PASSWORD=<your-password>` in the deployment environment
3. Deploy — on first boot, `init_db()` hashes and stores the password in `app_config`
4. Verify the lock screen appears before app content
5. Remove or rotate `APP_PASSWORD` env var after first boot (optional but recommended)

**Rollback**: Remove the lock screen block from `app.py` and redeploy. The `app_config` table is harmless if left in place.

## Open Questions

- None — all decisions are made.
