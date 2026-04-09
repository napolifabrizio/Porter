## MODIFIED Requirements

### Requirement: Product record contains required fields
Each product record SHALL store: `url` (unique), `name`, `description`, `initial_price`, `current_price`, `last_checked` (ISO 8601 datetime string), `list_id` (integer FK referencing `lists.id`, non-nullable, defaults to 1), and `currency` (display symbol string, non-nullable, defaults to `"R$"`).

#### Scenario: Product saved with all fields including currency
- **WHEN** a product is successfully scraped and saved
- **THEN** all eight fields (including `currency`) are written to the database in a single insert

#### Scenario: Product saved without explicit list_id defaults to Standard
- **WHEN** a product is saved without specifying a list_id
- **THEN** the stored record has `list_id = 1`

#### Scenario: Duplicate URL rejected
- **WHEN** the user attempts to add a URL that is already in the database
- **THEN** the system rejects the insert and surfaces an error message to the user without crashing

### Requirement: Existing databases are migrated to include the currency column
The system SHALL add the `currency` column to existing databases that lack it, defaulting all pre-existing rows to `"R$"`.

#### Scenario: Migration adds currency column
- **WHEN** the application starts and `porter.db` exists but lacks the `currency` column
- **THEN** the column is added with `DEFAULT 'R$'` and all existing rows are set to `"R$"`

#### Scenario: No migration on fresh database
- **WHEN** the application starts and `porter.db` does not exist
- **THEN** the `currency` column is present from the initial CREATE TABLE — no migration step runs
