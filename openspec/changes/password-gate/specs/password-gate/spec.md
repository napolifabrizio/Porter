## ADDED Requirements

### Requirement: App is protected by a password gate
The system SHALL display a lock screen before any app content on every new session. The lock screen SHALL contain a password input field and a submit button. The system SHALL NOT render any part of the main application until the user has authenticated in the current session.

#### Scenario: Unauthenticated user sees only the lock screen
- **WHEN** a user opens the app without an active authenticated session
- **THEN** only the lock screen is shown; no product list, sidebar, or other app content is rendered

#### Scenario: Correct password grants access
- **WHEN** the user enters the correct password and submits
- **THEN** the session is marked as authenticated and the full app is rendered

#### Scenario: Wrong password shows error
- **WHEN** the user enters an incorrect password and submits
- **THEN** an error message is shown and the lock screen remains; no app content is rendered

#### Scenario: Empty password submission is rejected
- **WHEN** the user submits the password form with an empty input
- **THEN** a warning is shown and no authentication attempt is made

### Requirement: Password hash is stored in the database using bcrypt
The system SHALL store the password as a bcrypt hash in the `app_config` SQLite table under the key `password_hash`. The plaintext password SHALL never be persisted. Verification SHALL use bcrypt comparison.

#### Scenario: Hash stored on first boot
- **WHEN** `init_db()` runs and no `password_hash` exists in `app_config` and `APP_PASSWORD` is set in the environment
- **THEN** the password is hashed with bcrypt and stored in `app_config` under key `password_hash`

#### Scenario: Seeding skipped on subsequent boots
- **WHEN** `init_db()` runs and a `password_hash` already exists in `app_config`
- **THEN** the existing hash is left unchanged regardless of the `APP_PASSWORD` env var

#### Scenario: Password verification uses bcrypt
- **WHEN** the user submits a password on the lock screen
- **THEN** the system compares it against the stored hash using `bcrypt.checkpw`; the plaintext is never stored

### Requirement: Authentication state is session-scoped
The system SHALL track authentication using Streamlit session state. Authentication SHALL be lost when the session ends (tab close or page refresh). There SHALL be no logout mechanism.

#### Scenario: Authenticated session persists within the same tab
- **WHEN** a user authenticates and navigates within the same Streamlit session
- **THEN** they remain authenticated without re-entering the password

#### Scenario: New session requires re-authentication
- **WHEN** a user closes and reopens the browser tab
- **THEN** a new session starts unauthenticated and the lock screen is shown again
