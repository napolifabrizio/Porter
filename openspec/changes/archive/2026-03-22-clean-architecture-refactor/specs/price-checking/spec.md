## MODIFIED Requirements

### Requirement: Price check re-scrapes all tracked products
The system SHALL re-scrape the current price for every product when a price check is triggered via `PriceChecker(scraper, repo).check_all_prices(products)`. `PriceChecker` SHALL receive a `ProductScraper` protocol and a `ProductRepository` protocol via its constructor — not the concrete `Scraper` and `Database` classes. All behavioral requirements (update, error handling, results) are unchanged.

#### Scenario: All products updated on check
- **WHEN** the user triggers a price check and all products scrape successfully
- **THEN** `current_price` and `last_checked` are updated for every product

#### Scenario: Failed scrape does not abort remaining checks
- **WHEN** scraping one product fails during a price check
- **THEN** the system records the error for that product, continues checking remaining products, and reports which products failed at the end

## ADDED Requirements

### Requirement: Price-drop rule is defined in the domain layer
The drop threshold constant (`DROP_THRESHOLD = 0.05`) and the evaluation logic SHALL live in `porter.domain.price_rules` as a pure function with no external dependencies. `PriceChecker` SHALL delegate to this function instead of computing the drop inline.

#### Scenario: Domain rule used by checker
- **WHEN** `PriceChecker.check_all_prices` evaluates whether a price dropped
- **THEN** it calls the function from `porter.domain.price_rules` to determine the result

#### Scenario: Domain rule is independently testable
- **WHEN** `porter.domain.price_rules` is imported in isolation (no scraper, no database)
- **THEN** the drop evaluation function can be called with two floats and returns a `(dropped: bool, change_pct: float)` tuple
