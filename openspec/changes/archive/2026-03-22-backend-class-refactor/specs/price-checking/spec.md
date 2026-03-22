## MODIFIED Requirements

### Requirement: Price check re-scrapes all tracked products
The system SHALL re-scrape the current price for every product when a price check is triggered via `PriceChecker(scraper, db).check_all_prices(products)`. `PriceChecker` SHALL receive a `Scraper` and `Database` instance via its constructor. All behavioral requirements (update, error handling, results) are unchanged.

#### Scenario: All products updated on check
- **WHEN** the user triggers a price check and all products scrape successfully
- **THEN** `current_price` and `last_checked` are updated for every product

#### Scenario: Failed scrape does not abort remaining checks
- **WHEN** scraping one product fails during a price check
- **THEN** the system records the error for that product, continues checking remaining products, and reports which products failed at the end
