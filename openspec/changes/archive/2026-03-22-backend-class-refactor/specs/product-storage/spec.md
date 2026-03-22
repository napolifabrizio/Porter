## MODIFIED Requirements

### Requirement: Products are persisted in SQLite
The system SHALL store all tracked products in a local SQLite database via the `Database` class. Callers SHALL instantiate `Database(db_path)` (defaulting to `Path("porter.db")`) and call methods on the instance. The database SHALL be created automatically on first run if it does not exist.

#### Scenario: Database initialized on first run
- **WHEN** the application starts and `porter.db` does not exist
- **THEN** the system creates the file and applies the schema automatically

#### Scenario: Database reused on subsequent runs
- **WHEN** the application starts and `porter.db` already exists
- **THEN** the system connects to the existing database without modifying existing data
