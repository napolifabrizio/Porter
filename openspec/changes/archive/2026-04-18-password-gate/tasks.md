## 1. Dependencies

- [x] 1.1 Add `bcrypt` to `pyproject.toml` dependencies and run `poetry install`

## 2. Database

- [x] 2.1 Add `app_config` table creation (`key TEXT PRIMARY KEY, value TEXT NOT NULL`) to `Database.init_db()` in `infrastructure/database.py`
- [x] 2.2 Add `get_config(key) -> str | None` method to `Database`
- [x] 2.3 Add `set_config(key, value)` method to `Database`

## 3. Auth Infrastructure

- [x] 3.1 Create `source/porter/infrastructure/auth.py` with `verify_password(db, raw_password) -> bool` using `bcrypt.checkpw`
- [x] 3.2 Add `seed_password_if_missing(db)` to `auth.py` — reads `APP_PASSWORD` env var, hashes with bcrypt, stores via `db.set_config("password_hash", hash)` only if no hash exists yet

## 4. First-Boot Seeding

- [x] 4.1 Call `seed_password_if_missing(db)` inside `AppService.__init__()` (after `init_db()`) so the hash is seeded before any request is served

## 5. Lock Screen UI

- [x] 5.1 Add auth check block at the top of `ui/app.py` (before `svc = AppService()` and all other rendering): if `st.session_state.get("authenticated")` is falsy, render the lock screen and call `st.stop()`
- [x] 5.2 Lock screen renders: `st.title("Porter")`, a password input (`type="password"`), and a login button
- [x] 5.3 On submit: if input is empty show `st.warning`; else call `verify_password` — on success set `st.session_state["authenticated"] = True` and `st.rerun()`; on failure show `st.error("Wrong password.")`
