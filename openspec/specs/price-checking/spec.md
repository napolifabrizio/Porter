## ADDED Requirements

### Requirement: Price check re-scrapes all tracked products
The system SHALL re-scrape the current price for every product when a price check is triggered via `PriceChecker(scraper, repo).check_all_prices(products)`. `PriceChecker` SHALL receive a `ProductScraper` protocol and a `ProductRepository` protocol via its constructor — not the concrete `Scraper` and `Database` classes. All products SHALL be checked concurrently (using a thread pool), not sequentially. Results SHALL be returned in the same order as the input `products` list regardless of completion order.

#### Scenario: All products updated on check
- **WHEN** the user triggers a price check and all products scrape successfully
- **THEN** `current_price` and `last_checked` are updated for every product

#### Scenario: Failed scrape does not abort remaining checks
- **WHEN** scraping one product fails during a price check
- **THEN** the system records the error for that product, continues checking remaining products, and reports which products failed at the end

#### Scenario: Products are checked concurrently
- **WHEN** a price check is triggered for multiple products
- **THEN** all products are fetched and scraped at the same time (in parallel threads), not one after another

#### Scenario: Results preserve input order
- **WHEN** a price check completes for a list of products
- **THEN** the returned results list matches the order of the input products list, regardless of which product finished scraping first

### Requirement: Price-drop rule is defined in the domain layer
The drop threshold constant (`DROP_THRESHOLD = 0.05`) and the evaluation logic SHALL live in `porter.domain.price_rules` as a pure function with no external dependencies. `PriceChecker` SHALL delegate to this function instead of computing the drop inline.

#### Scenario: Domain rule used by checker
- **WHEN** `PriceChecker.check_all_prices` evaluates whether a price dropped
- **THEN** it calls the function from `porter.domain.price_rules` to determine the result

#### Scenario: Domain rule is independently testable
- **WHEN** `porter.domain.price_rules` is imported in isolation (no scraper, no database)
- **THEN** the drop evaluation function can be called with two floats and returns a `(dropped: bool, change_pct: float)` tuple

### Requirement: A price drop is detected when current price is ≥ 5% below initial price
The system SHALL flag a product as "price dropped" when `(initial_price − current_price) / initial_price ≥ 0.05`.

#### Scenario: Drop of exactly 5% is flagged
- **WHEN** `initial_price` is `100.00` and `current_price` is `95.00`
- **THEN** the product is flagged as dropped

#### Scenario: Drop below 5% is not flagged
- **WHEN** `initial_price` is `100.00` and `current_price` is `96.00`
- **THEN** the product is NOT flagged as dropped

#### Scenario: Price increase is not flagged
- **WHEN** `current_price` is greater than `initial_price`
- **THEN** the product is NOT flagged as dropped

### Requirement: Check results include per-product status
The system SHALL return a result for each product containing: the product record, whether it dropped, the percentage change, and any error message if the check failed.

#### Scenario: Successful check result
- **WHEN** a product's price was successfully re-scraped
- **THEN** the result includes `dropped: bool`, `change_pct: float`, and `error: None`

#### Scenario: Failed check result
- **WHEN** a product's price could not be scraped
- **THEN** the result includes `error: str` describing the failure and `dropped: False`
