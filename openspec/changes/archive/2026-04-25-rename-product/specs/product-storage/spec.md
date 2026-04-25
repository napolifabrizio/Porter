## MODIFIED Requirements

### Requirement: A ProductRepository protocol defines the storage contract
The system SHALL define a `ProductRepository` Protocol in `porter.application.ports` with the following methods: `init_db() -> None`, `add_product(scraped: ScrapedData, url: str, list_id: int | None = None) -> Product`, `list_products(list_id: int | None = None) -> list[Product]`, `update_price(product_id: int, new_price: float) -> None`, `update_name(product_id: int, name: str) -> None`, and `remove_product(product_id: int) -> None`. Any class implementing these methods SHALL satisfy the protocol without explicit inheritance.

#### Scenario: Database satisfies protocol structurally
- **WHEN** `porter.infrastructure.database.Database` is checked against `ProductRepository`
- **THEN** it is recognized as a valid implementation without importing or inheriting from `ProductRepository`

#### Scenario: Name updated without touching price fields
- **WHEN** `update_name(product_id=1, name="New Name")` is called
- **THEN** only the `name` column is updated; `initial_price`, `current_price`, and `last_checked` remain unchanged
