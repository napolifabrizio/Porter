## Context

Porter currently uses a raw `sqlite3`-based `Database` class in `infrastructure/database.py`. It implements both `ProductRepository` and `WatchListRepository` protocols using hand-written SQL and manual connection management. The PostgreSQL schema is already in place externally — the implementation only needs to connect and issue queries.

## Goals / Non-Goals

**Goals:**
- Replace `sqlite3` with SQLAlchemy ORM backed by PostgreSQL
- Keep the same public interface (`Database` class implements both repository protocols)
- Read connection string from `DATABASE_URL` env var
- Keep `last_checked` as `str` at the Pydantic boundary (stored as `String` in SQLAlchemy)
- Remove all table-creation and schema-migration logic

**Non-Goals:**
- Alembic setup or schema migration tooling
- Changing `Product`, `WatchList`, or `ScrapedData` Pydantic models
- Splitting `Database` into separate classes per protocol
- Adding connection pooling configuration beyond SQLAlchemy defaults

## Decisions

### 1. SQLAlchemy ORM with internal mapped classes

Define SQLAlchemy `DeclarativeBase` models (`ListRow`, `ProductRow`, `AppConfigRow`) internal to `database.py`. These are never exported. At every method boundary, map ORM rows → Pydantic DTOs before returning.

**Why over Core/`text()`:** ORM gives type-safe column access and cleaner query composition. `text()` would just be sqlite3 with extra steps.

### 2. Per-method `Session` context manager

Each method opens and closes its own `Session` via `with Session(engine) as session:`, mirroring the current per-method `_connect()` pattern.

**Why over scoped/shared session:** Streamlit rerenders trigger method calls independently; a shared session would require lifecycle management. Per-method sessions are simpler and safe.

### 3. `last_checked` stored as `String`

`Product.last_checked` is typed `str` (ISO datetime string) throughout the codebase and rendered directly in the UI. Store it as `String` in the ORM model to avoid a conversion layer.

**Why not `DateTime`:** Would require changing the Pydantic model and UI rendering — out of scope for this change.

### 4. Remove `init_db()` entirely

The PostgreSQL schema already exists. `init_db()` is removed from `Database`, from the `ProductRepository` protocol in `ports.py`, and from `AppService.__init__`.

**Why:** Table creation doesn't belong in application code when schema is managed externally.

### 5. `DATABASE_URL` read at `Database.__init__`

`Database.__init__` reads `os.environ["DATABASE_URL"]` and creates the SQLAlchemy engine. `AppService` does not need to change its signature.

**Alternative considered:** Pass URL as constructor arg from `AppService`. Rejected — adds parameter threading with no benefit since there's only one database.

### 6. `IntegrityError` handling

Replace `sqlite3.IntegrityError` with `sqlalchemy.exc.IntegrityError` in `add_product` and `create_list`. Same behavior, different import.

## Risks / Trade-offs

- **`Standard` list seeding removed** → The `INSERT OR IGNORE INTO lists (id, name) VALUES (1, 'Standard')` seed must exist in the PostgreSQL schema before the app runs. If not, `list_id=1` references will fail with a FK violation. Mitigation: document this as a prerequisite; the user confirmed the DB is already set up.
- **`last_checked` as String in PostgreSQL** → No timezone-awareness at the DB level. Values are stored as arbitrary text. Mitigation: acceptable for this app's scale; can be revisited if needed.
- **No connection pool tuning** → SQLAlchemy defaults (5 connections, overflow 10) may be suboptimal. Mitigation: not a concern for a single-user Streamlit app.

## Open Questions

*(none — all decisions resolved during exploration)*
