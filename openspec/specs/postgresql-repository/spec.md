## ADDED Requirements

### Requirement: Connect to PostgreSQL via DATABASE_URL
The system SHALL read a `DATABASE_URL` environment variable and use it to create a SQLAlchemy engine connected to PostgreSQL. The application SHALL fail with a clear error if `DATABASE_URL` is not set.

#### Scenario: App starts with DATABASE_URL set
- **WHEN** `DATABASE_URL` is present in the environment
- **THEN** the `Database` class creates a SQLAlchemy engine and session factory successfully

#### Scenario: App starts without DATABASE_URL
- **WHEN** `DATABASE_URL` is missing from the environment
- **THEN** the application raises a `KeyError` or descriptive `ValueError` on startup

### Requirement: Product CRUD via SQLAlchemy ORM
The system SHALL implement `ProductRepository` operations (`add_product`, `list_products`, `update_price`, `remove_product`) using SQLAlchemy ORM sessions against PostgreSQL, with the same behavior and return types as the previous SQLite implementation.

#### Scenario: Add a new product
- **WHEN** `add_product(scraped, url)` is called with a URL not already tracked
- **THEN** a new row is inserted into `products` and a `Product` Pydantic model is returned with `initial_price == current_price`

#### Scenario: Add a duplicate product
- **WHEN** `add_product(scraped, url)` is called with a URL already in the database
- **THEN** `sqlalchemy.exc.IntegrityError` is caught and re-raised as `ValueError`

#### Scenario: List products filtered by list
- **WHEN** `list_products(list_id=N)` is called
- **THEN** only products with `list_id = N` are returned as `Product` Pydantic models

#### Scenario: Update product price
- **WHEN** `update_price(product_id, new_price)` is called
- **THEN** the product's `current_price` and `last_checked` are updated; `initial_price` is never modified

#### Scenario: Remove a product
- **WHEN** `remove_product(product_id)` is called
- **THEN** the product row is deleted from the database

### Requirement: WatchList CRUD via SQLAlchemy ORM
The system SHALL implement `WatchListRepository` operations (`create_list`, `list_all_lists`, `delete_list`, `move_product_to_list`) using SQLAlchemy ORM sessions, with identical behavior to the previous SQLite implementation.

#### Scenario: Create a new list
- **WHEN** `create_list(name)` is called with a unique name
- **THEN** a new row is inserted into `lists` and a `WatchList` Pydantic model is returned

#### Scenario: Create a duplicate list
- **WHEN** `create_list(name)` is called with an existing name
- **THEN** `sqlalchemy.exc.IntegrityError` is caught and re-raised as `ValueError`

#### Scenario: Delete a list reassigns products
- **WHEN** `delete_list(list_id)` is called
- **THEN** all products in that list are moved to `list_id = 1` before the list row is deleted

#### Scenario: Move product to another list
- **WHEN** `move_product_to_list(product_id, list_id)` is called with a valid target list
- **THEN** the product's `list_id` is updated

#### Scenario: Move product to non-existent list
- **WHEN** `move_product_to_list(product_id, list_id)` is called with a `list_id` that does not exist
- **THEN** a `ValueError` is raised

### Requirement: App config stored in PostgreSQL
The system SHALL implement `get_config(key)` and `set_config(key, value)` using SQLAlchemy ORM against the `app_config` table, preserving upsert semantics.

#### Scenario: Get existing config value
- **WHEN** `get_config(key)` is called for a key that exists
- **THEN** the stored string value is returned

#### Scenario: Get missing config value
- **WHEN** `get_config(key)` is called for a key that does not exist
- **THEN** `None` is returned

#### Scenario: Set config value (upsert)
- **WHEN** `set_config(key, value)` is called
- **THEN** the value is inserted if new, or updated if the key already exists
