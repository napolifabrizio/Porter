## 1. Dependencies & Environment

- [x] 1.1 Add `sqlalchemy` and `psycopg2-binary` to `pyproject.toml` via `poetry add`
- [x] 1.2 Add `DATABASE_URL` to `.env` with the local PostgreSQL connection string
- [x] 1.3 Add `DATABASE_URL=postgresql://user:password@localhost:5432/porter` placeholder to `.env.example`

## 2. Protocol Cleanup

- [x] 2.1 Remove `init_db()` from `ProductRepository` protocol in `application/ports.py`
- [x] 2.2 Remove `self._db.init_db()` call from `AppService.__init__` in `application/service.py`

## 3. Rewrite Database Layer

- [x] 3.1 Define SQLAlchemy `DeclarativeBase` and ORM models (`ListRow`, `ProductRow`, `AppConfigRow`) at the top of `infrastructure/database.py`
- [x] 3.2 Replace `Database.__init__` to read `DATABASE_URL` from env and create `engine` + `sessionmaker`
- [x] 3.3 Rewrite `add_product` using SQLAlchemy session, catching `sqlalchemy.exc.IntegrityError`
- [x] 3.4 Rewrite `list_products` using SQLAlchemy ORM query with optional `list_id` filter
- [x] 3.5 Rewrite `update_price` using SQLAlchemy session update
- [x] 3.6 Rewrite `remove_product` using SQLAlchemy session delete
- [x] 3.7 Rewrite `create_list` using SQLAlchemy session, catching `sqlalchemy.exc.IntegrityError`
- [x] 3.8 Rewrite `list_all_lists` using SQLAlchemy ORM query
- [x] 3.9 Rewrite `delete_list` (reassign products to list 1, then delete) using SQLAlchemy session
- [x] 3.10 Rewrite `move_product_to_list` using SQLAlchemy session, validating target list exists
- [x] 3.11 Rewrite `get_config` and `set_config` using SQLAlchemy session with upsert via `merge`

## 4. Validation

- [x] 4.1 Run the Streamlit app and verify products can be added, listed, and removed
- [x] 4.2 Verify `initial_price` is never modified when price is updated
- [x] 4.3 Verify watchlist creation, deletion, and product reassignment work correctly
- [x] 4.4 Verify authentication (`verify_password` via `get_config`) still works
