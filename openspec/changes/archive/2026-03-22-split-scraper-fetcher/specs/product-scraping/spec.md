## MODIFIED Requirements

### Requirement: Scraper extracts name, price, and description from any URL
The system SHALL attempt to extract product `name`, `price` (as a float), and `description` from a given URL via the `Scraper` class located at `porter.infrastructure.scraper`. The `Scraper` class SHALL satisfy the `ProductScraper` protocol defined in `porter.application.ports`. The `Scraper` SHALL receive an `HtmlFetcher` implementation via constructor injection and delegate HTTP fetching to it. The two-phase hybrid strategy (CSS selectors first, LLM fallback second) and all behavioral requirements are unchanged.

#### Scenario: Successful extraction via CSS selectors
- **WHEN** the page HTML contains recognizable structured fields (e.g., `[itemprop="price"]`, `h1`, `meta[name="description"]`)
- **THEN** the scraper returns the extracted data without calling the LLM

#### Scenario: LLM fallback triggered on partial extraction
- **WHEN** one or more fields are not found by CSS selectors
- **THEN** the scraper strips scripts/styles from the HTML, truncates to ~8000 characters, sends to LangChain LLM, and returns the LLM-extracted data

#### Scenario: Both methods fail
- **WHEN** neither CSS selectors nor the LLM can extract a valid price
- **THEN** the scraper raises a descriptive error that the UI can display to the user
