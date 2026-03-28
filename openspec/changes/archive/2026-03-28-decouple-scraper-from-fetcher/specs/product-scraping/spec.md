## MODIFIED Requirements

### Requirement: Scraper extracts name, price, and description from HTML
The system SHALL attempt to extract product `name`, `price` (as a float), and `description` from a given HTML string via the `Scraper` class located at `porter.infrastructure.scraper`. The `Scraper` class SHALL satisfy the `ProductScraper` protocol defined in `porter.application.ports`. The `Scraper` SHALL NOT accept or hold a reference to any HTTP fetcher — it SHALL receive pre-fetched HTML as a string parameter. The two-phase hybrid strategy (CSS selectors first, LLM fallback second) and all behavioral requirements are unchanged.

#### Scenario: Successful extraction via CSS selectors
- **WHEN** the provided HTML contains recognizable structured fields (e.g., `[itemprop="price"]`, `h1`, `meta[name="description"]`)
- **THEN** the scraper returns the extracted data without calling the LLM

#### Scenario: LLM fallback triggered on partial extraction
- **WHEN** one or more fields are not found by CSS selectors
- **THEN** the scraper strips scripts/styles from the HTML, truncates to ~8000 characters, sends to LangChain LLM, and returns the LLM-extracted data

#### Scenario: Both methods fail
- **WHEN** neither CSS selectors nor the LLM can extract a valid price
- **THEN** the scraper raises a descriptive error that the UI can display to the user

### Requirement: A ProductScraper protocol defines the scraping contract
The system SHALL define a `ProductScraper` Protocol in `porter.application.ports` with a single method `scrape(html: str) -> ScrapedData`. Any class that implements this method with the correct signature SHALL satisfy the protocol without explicit inheritance.

#### Scenario: Scraper satisfies protocol structurally
- **WHEN** `porter.infrastructure.scraper.Scraper` is checked against `ProductScraper`
- **THEN** it is recognized as a valid implementation without importing or inheriting from `ProductScraper`

#### Scenario: Scraper can be tested with raw HTML
- **WHEN** `Scraper().scrape(html)` is called with a valid HTML string
- **THEN** it returns a `ScrapedData` result without making any HTTP request

## REMOVED Requirements

### Requirement: HTTP requests use browser-like headers
**Reason**: HTTP fetching is no longer the responsibility of `Scraper`. This concern belongs exclusively to `html-fetching` / `HttpFetcher`.
**Migration**: No migration needed — `HttpFetcher` already handles browser-like headers and this requirement is fully covered by the `html-fetching` spec.
