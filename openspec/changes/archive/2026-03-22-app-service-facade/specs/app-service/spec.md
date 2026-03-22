## ADDED Requirements

### Requirement: AppService exposes a unified interface for all UI operations
The system SHALL provide an `AppService` class in `source/porter/service.py` that serves as the sole entry point for the UI layer to interact with the backend. `AppService` SHALL instantiate and wire all backend classes internally.

#### Scenario: Frontend imports only AppService
- **WHEN** the UI module (`app.py`) needs to perform any backend operation
- **THEN** it imports only `AppService` from `porter.service` and no other backend module

#### Scenario: AppService initializes all backend dependencies
- **WHEN** `AppService()` is instantiated
- **THEN** it creates `Database`, `Scraper`, and `PriceChecker` instances internally without requiring them as constructor arguments

### Requirement: AppService.track adds a product by URL
The system SHALL provide `AppService.track(url: str) -> Product` that fetches and scrapes the URL, saves the product to the database, and returns the saved `Product` record in a single call.

#### Scenario: Successful product tracking
- **WHEN** `track(url)` is called with a valid product URL
- **THEN** the product is scraped, saved to the database, and the saved `Product` is returned

#### Scenario: Duplicate URL rejected
- **WHEN** `track(url)` is called with a URL already in the database
- **THEN** a `ValueError` is raised and no duplicate is saved

#### Scenario: Scrape failure propagated
- **WHEN** `track(url)` is called and the scraper raises an error
- **THEN** the error propagates to the caller unchanged and nothing is saved

### Requirement: AppService.list_products returns all tracked products
The system SHALL provide `AppService.list_products() -> list[Product]` that returns all tracked products ordered by insertion time.

#### Scenario: Products returned in order
- **WHEN** `list_products()` is called
- **THEN** all tracked products are returned in insertion order

#### Scenario: Empty list on no products
- **WHEN** `list_products()` is called and no products exist
- **THEN** an empty list is returned without error

### Requirement: AppService.check_all_prices checks prices without requiring product list from caller
The system SHALL provide `AppService.check_all_prices() -> list[CheckResult]` that loads products internally and delegates to `PriceChecker`. The caller SHALL NOT be required to supply the product list.

#### Scenario: Prices checked for all products
- **WHEN** `check_all_prices()` is called
- **THEN** the service loads all products from the database and returns a `CheckResult` for each

#### Scenario: Empty result on no products
- **WHEN** `check_all_prices()` is called and no products are tracked
- **THEN** an empty list is returned without error
