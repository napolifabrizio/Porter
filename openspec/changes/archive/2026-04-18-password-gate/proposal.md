## Why

Porter is being deployed to AWS and will be publicly accessible via a URL. Without any access control, anyone who discovers the URL can view and manipulate the watchlist. A simple password gate provides the minimal protection needed for a personal app.

## What Changes

- A lock screen is shown on every new session before any app content is rendered
- The user must enter the correct password to access Porter
- The password hash is stored in the SQLite database using bcrypt
- The app seeds the hash on first boot from the `APP_PASSWORD` environment variable
- Authentication state lives in Streamlit session state (cleared when the tab is closed)

## Capabilities

### New Capabilities
- `password-gate`: Lock screen that blocks access to the app until the user provides the correct password; bcrypt hash stored in DB and seeded from env var on first boot

### Modified Capabilities
- `tracker-ui`: The UI gains a pre-render authentication check that halts rendering if the session is not authenticated

## Impact

- **New dependency**: `bcrypt` package added to `pyproject.toml`
- **New file**: `source/porter/infrastructure/auth.py` — bcrypt verify/seed helpers
- **Modified**: `source/porter/infrastructure/database.py` — new `app_config` table + `get_config`/`set_config` methods + password seeding in `init_db()`
- **Modified**: `source/porter/ui/app.py` — lock screen block at the top of the file
- **New env var**: `APP_PASSWORD` — plain-text password set in AWS environment; hashed and stored in DB on first boot
