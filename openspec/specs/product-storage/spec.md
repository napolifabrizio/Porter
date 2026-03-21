## ADDED Requirements

### Requirement: Products are persisted in SQLite
The system SHALL store all tracked products in a local SQLite database file (`porter.db`). The database SHALL be created automatically on first run if it does not exist.

#### Scenario: Database initialized on first run
- **WHEN** the application starts and `porter.db` does not exist
- **THEN** the system creates the file and applies the schema automatically

#### Scenario: Database reused on subsequent runs
- **WHEN** the application starts and `porter.db` already exists
- **THEN** the system connects to the existing database without modifying existing data

### Requirement: Product record contains required fields
Each product record SHALL store: `url` (unique), `name`, `description`, `initial_price`, `current_price`, and `last_checked` (ISO 8601 datetime string).

#### Scenario: Product saved with all fields
- **WHEN** a product is successfully scraped from a URL
- **THEN** all six fields are written to the database in a single insert

#### Scenario: Duplicate URL rejected
- **WHEN** the user attempts to add a URL that is already in the database
- **THEN** the system rejects the insert and surfaces an error message to the user without crashing

### Requirement: Current price is updatable
The system SHALL update `current_price` and `last_checked` for an existing product without changing `initial_price`.

#### Scenario: Price updated on check
- **WHEN** a price check is triggered and a new price is scraped for a product
- **THEN** `current_price` and `last_checked` are updated; `initial_price` remains unchanged

### Requirement: Products can be listed
The system SHALL return all stored products ordered by insertion time (ascending).

#### Scenario: Empty list returned when no products exist
- **WHEN** the database has no products
- **THEN** the system returns an empty list without error

#### Scenario: All products returned
- **WHEN** the database contains one or more products
- **THEN** the system returns all of them in insertion order
