## Requirements

### Requirement: Products are persisted in SQLite
The system SHALL store all tracked products in a local SQLite database via the `Database` class located at `porter.infrastructure.database`. The `Database` class SHALL satisfy both the `ProductRepository` and `WatchListRepository` protocols defined in `porter.application.ports`. All behavioral requirements (schema, fields, duplicate handling) are unchanged, with the addition of a `list_id` foreign key on each product and a new `lists` table.

#### Scenario: Database initialized on first run
- **WHEN** the application starts and `porter.db` does not exist
- **THEN** the system creates the file, creates the `lists` and `products` tables, and inserts the Standard list automatically

#### Scenario: Database reused on subsequent runs
- **WHEN** the application starts and `porter.db` already exists
- **THEN** the system connects to the existing database without modifying existing data; if the `list_id` or `currency` columns are absent they are added via migration

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

### Requirement: Current price is updatable
The system SHALL update `current_price` and `last_checked` for an existing product without changing `initial_price`.

#### Scenario: Price updated on check
- **WHEN** a price check is triggered and a new price is scraped for a product
- **THEN** `current_price` and `last_checked` are updated; `initial_price` remains unchanged

### Requirement: Products can be listed with optional list filter
The system SHALL return stored products ordered by insertion time (ascending). An optional `list_id` parameter SHALL filter the results to only products belonging to that list. When `list_id` is `None`, all products are returned.

#### Scenario: All products returned when no filter given
- **WHEN** `list_products()` is called without a list_id
- **THEN** all tracked products are returned in insertion order

#### Scenario: Filtered products returned when list_id given
- **WHEN** `list_products(list_id=2)` is called
- **THEN** only products with `list_id = 2` are returned in insertion order

#### Scenario: Empty list returned when no products in list
- **WHEN** `list_products(list_id=X)` is called and list X has no products
- **THEN** an empty list is returned without error

### Requirement: A ProductRepository protocol defines the storage contract
The system SHALL define a `ProductRepository` Protocol in `porter.application.ports` with the following methods: `init_db() -> None`, `add_product(scraped: ScrapedData, url: str, list_id: int | None = None) -> Product`, `list_products(list_id: int | None = None) -> list[Product]`, `update_price(product_id: int, new_price: float) -> None`, and `remove_product(product_id: int) -> None`. Any class implementing these methods SHALL satisfy the protocol without explicit inheritance.

#### Scenario: Database satisfies protocol structurally
- **WHEN** `porter.infrastructure.database.Database` is checked against `ProductRepository`
- **THEN** it is recognized as a valid implementation without importing or inheriting from `ProductRepository`

### Requirement: A WatchListRepository protocol defines the list storage contract
The system SHALL define a `WatchListRepository` Protocol in `porter.application.ports` with the following methods: `create_list(name: str) -> WatchList`, `list_all_lists() -> list[WatchList]`, `delete_list(list_id: int) -> None`, and `move_product_to_list(product_id: int, list_id: int) -> None`. The `Database` class SHALL satisfy this protocol structurally.

#### Scenario: Database satisfies WatchListRepository structurally
- **WHEN** `porter.infrastructure.database.Database` is checked against `WatchListRepository`
- **THEN** it is recognized as a valid implementation without importing or inheriting from `WatchListRepository`
