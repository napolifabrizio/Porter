## MODIFIED Requirements

### Requirement: AppService.track adds a product by URL
The system SHALL provide `AppService.track(url: str, list_id: int | None = None) -> TrackResult` that fetches and scrapes the URL, saves the product to the specified list (defaulting to Standard when `list_id` is `None`), and returns a `TrackResult`.

#### Scenario: Successful product tracking to specific list
- **WHEN** `track(url, list_id=2)` is called with a valid product URL and an existing list ID
- **THEN** the product is scraped, saved to list 2, and the saved `TrackResult` is returned

#### Scenario: Successful product tracking defaults to Standard
- **WHEN** `track(url)` is called without a list_id
- **THEN** the product is scraped, saved to the Standard list, and returned

#### Scenario: Duplicate URL rejected
- **WHEN** `track(url)` is called with a URL already in the database
- **THEN** a `ValueError` is raised and no duplicate is saved

#### Scenario: Scrape failure propagated
- **WHEN** `track(url)` is called and the scraper raises an error
- **THEN** the error propagates to the caller unchanged and nothing is saved

### Requirement: AppService.list_products returns products filtered by list
The system SHALL provide `AppService.list_products(list_id: int | None = None) -> list[Product]`. When `list_id` is provided, only products belonging to that list are returned. When `list_id` is `None`, all products are returned.

#### Scenario: All products returned when no list_id given
- **WHEN** `list_products()` is called without a list_id
- **THEN** all tracked products are returned in insertion order

#### Scenario: Filtered products returned
- **WHEN** `list_products(list_id=2)` is called
- **THEN** only products in list 2 are returned

#### Scenario: Empty list on no products
- **WHEN** `list_products()` is called and no products exist
- **THEN** an empty list is returned without error

## ADDED Requirements

### Requirement: AppService exposes list management operations
The system SHALL provide the following methods on `AppService` for managing watchlists:
- `create_list(name: str) -> WatchList` — creates a new named list
- `list_all_lists() -> list[WatchList]` — returns all lists
- `delete_list(list_id: int) -> None` — deletes a list; products are moved to Standard
- `move_product(product_id: int, target_list_id: int) -> None` — moves a product to another list

Attempting to delete the Standard list (id = 1) SHALL raise a `ValueError`.

#### Scenario: List created via service
- **WHEN** `create_list("Foods")` is called
- **THEN** a new `WatchList` with name "Foods" is returned and persisted

#### Scenario: All lists returned
- **WHEN** `list_all_lists()` is called
- **THEN** a list containing at least the Standard list is returned

#### Scenario: List deleted and products fall back to Standard
- **WHEN** `delete_list(list_id=2)` is called and list 2 has products
- **THEN** those products' `list_id` is updated to 1, then the list is deleted

#### Scenario: Standard list deletion rejected by service
- **WHEN** `delete_list(list_id=1)` is called
- **THEN** a `ValueError` is raised and the Standard list is not deleted

#### Scenario: Product moved to another list
- **WHEN** `move_product(product_id=5, target_list_id=3)` is called
- **THEN** the product's `list_id` is updated to 3
