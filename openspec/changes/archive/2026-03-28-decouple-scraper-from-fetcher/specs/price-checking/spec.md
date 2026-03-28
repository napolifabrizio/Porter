## MODIFIED Requirements

### Requirement: Price check re-scrapes all tracked products
The system SHALL re-scrape the current price for every product when a price check is triggered via `PriceChecker(scraper, repo, fetcher).check_all_prices(products)`. `PriceChecker` SHALL receive a `ProductScraper` protocol, a `ProductRepository` protocol, and an `HtmlFetcher` protocol via its constructor — not concrete implementations. For each product, `PriceChecker` SHALL fetch the HTML via `fetcher.fetch(product.url)` and then parse it via `scraper.scrape(html)`. All products SHALL be checked concurrently (using a thread pool), not sequentially. Results SHALL be returned in the same order as the input `products` list regardless of completion order.

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

#### Scenario: PriceChecker depends only on protocols
- **WHEN** `PriceChecker` is constructed
- **THEN** it accepts `scraper: ProductScraper`, `repo: ProductRepository`, and `fetcher: HtmlFetcher` — no concrete infrastructure classes
