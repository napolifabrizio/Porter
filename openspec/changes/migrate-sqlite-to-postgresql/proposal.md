## Why

SQLite is a file-based database unsuitable for production deployments. Migrating to PostgreSQL with SQLAlchemy gives us a production-grade database engine and an ORM that eliminates raw SQL and manual connection management.

## What Changes

- Add `sqlalchemy` and `psycopg2-binary` dependencies via Poetry
- Add `DATABASE_URL` environment variable for PostgreSQL connection configuration
- Rewrite `infrastructure/database.py` using SQLAlchemy ORM — no raw `sqlite3`, no manual SQL, no table creation logic
- Remove `init_db()` from `ProductRepository` protocol and `AppService` (schema managed externally)
- Update `.env.example` with `DATABASE_URL` placeholder

## Capabilities

### New Capabilities

- `postgresql-repository`: SQLAlchemy-based implementation of `ProductRepository` and `WatchListRepository` backed by PostgreSQL

### Modified Capabilities

*(none — no spec-level behavior changes; only the infrastructure implementation changes)*

## Impact

- `pyproject.toml`: new dependencies `sqlalchemy`, `psycopg2-binary`
- `source/porter/infrastructure/database.py`: full rewrite
- `source/porter/application/ports.py`: remove `init_db()` from `ProductRepository`
- `source/porter/application/service.py`: remove `self._db.init_db()` call
- `.env` / `.env.example`: add `DATABASE_URL`
- `porter.db` SQLite file: no longer used
