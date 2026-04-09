## MODIFIED Requirements

### Requirement: Scraper extracts name, price, and description from HTML
The system SHALL attempt to extract product `name`, `price` (as a float), `currency` (as a display symbol string), and `description` from a given HTML string via the `Scraper` class located at `porter.infrastructure.scraper`. The `Scraper` class SHALL satisfy the `ProductScraper` protocol defined in `porter.application.ports`. The `Scraper` SHALL NOT accept or hold a reference to any HTTP fetcher — it SHALL receive pre-fetched HTML as a string parameter. The two-phase hybrid strategy (CSS selectors first, LLM fallback second) and all behavioral requirements are unchanged.

#### Scenario: Successful extraction via CSS selectors
- **WHEN** the provided HTML contains recognizable structured fields (e.g., `[itemprop="price"]`, `h1`, `meta[name="description"]`)
- **THEN** the scraper returns the extracted data including a `currency` symbol without calling the LLM

#### Scenario: LLM fallback triggered on partial extraction
- **WHEN** one or more fields are not found by CSS selectors
- **THEN** the scraper strips scripts/styles from the HTML, truncates to ~8000 characters, sends to LangChain LLM, and returns the LLM-extracted data including a `currency` symbol

#### Scenario: Both methods fail
- **WHEN** neither CSS selectors nor the LLM can extract a valid price
- **THEN** the scraper raises a descriptive error that the UI can display to the user
