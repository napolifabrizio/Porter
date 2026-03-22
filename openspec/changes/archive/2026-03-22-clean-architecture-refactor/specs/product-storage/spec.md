## MODIFIED Requirements

### Requirement: Products are persisted in SQLite
The system SHALL store all tracked products in a local SQLite database via the `Database` class located at `porter.infrastructure.database`. The `Database` class SHALL satisfy the `ProductRepository` protocol defined in `porter.application.ports`. All behavioral requirements (schema, fields, duplicate handling) are unchanged.

#### Scenario: Database initialized on first run
- **WHEN** the application starts and `porter.db` does not exist
- **THEN** the system creates the file and applies the schema automatically

#### Scenario: Database reused on subsequent runs
- **WHEN** the application starts and `porter.db` already exists
- **THEN** the system connects to the existing database without modifying existing data

## ADDED Requirements

### Requirement: A ProductRepository protocol defines the storage contract
The system SHALL define a `ProductRepository` Protocol in `porter.application.ports` with the following methods: `init_db() -> None`, `add_product(scraped: ScrapedData, url: str) -> Product`, `list_products() -> list[Product]`, and `update_price(product_id: int, new_price: float) -> None`. Any class implementing these methods SHALL satisfy the protocol without explicit inheritance.

#### Scenario: Database satisfies protocol structurally
- **WHEN** `porter.infrastructure.database.Database` is checked against `ProductRepository`
- **THEN** it is recognized as a valid implementation without importing or inheriting from `ProductRepository`
