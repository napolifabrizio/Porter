## ADDED Requirements

### Requirement: HttpFetcher retrieves raw HTML from a URL
The system SHALL provide an `HttpFetcher` class at `porter.infrastructure.fetcher` that fetches the HTML content of a given URL and returns it as a string. `HttpFetcher` SHALL satisfy the `HtmlFetcher` protocol defined in `porter.application.ports`.

#### Scenario: Successful fetch returns HTML string
- **WHEN** a valid URL is passed to `HttpFetcher.fetch(url)`
- **THEN** the method returns the page HTML as a string

#### Scenario: Network error raises descriptive error
- **WHEN** the HTTP request fails (timeout, DNS error, non-200 status)
- **THEN** `HttpFetcher.fetch` raises a `RuntimeError` with a message describing the failure

### Requirement: Requests use browser-like headers and impersonation
The system SHALL send HTTP requests with a realistic `User-Agent`, `Accept`, and `Accept-Language` header, and SHALL use `curl_cffi` browser impersonation to reduce the likelihood of being blocked by anti-bot measures.

#### Scenario: Request includes User-Agent header
- **WHEN** `HttpFetcher.fetch` is called with any URL
- **THEN** the HTTP request includes a non-empty `User-Agent` header mimicking a real browser

### Requirement: Tracking query parameters are stripped before fetching
The system SHALL remove known tracking and analytics parameters (e.g., `utm_source`, `gclid`, `fbclid`) from the URL before making the HTTP request.

#### Scenario: Tracking params removed from URL
- **WHEN** the URL contains query parameters such as `utm_source` or `gclid`
- **THEN** those parameters are removed and the request is made to the cleaned URL

#### Scenario: Non-tracking params preserved
- **WHEN** the URL contains query parameters unrelated to tracking
- **THEN** those parameters are preserved in the request URL

### Requirement: An HtmlFetcher protocol defines the fetching contract
The system SHALL define an `HtmlFetcher` Protocol in `porter.application.ports` with a single method `fetch(url: str) -> str`. Any class implementing this method SHALL satisfy the protocol without explicit inheritance.

#### Scenario: HttpFetcher satisfies protocol structurally
- **WHEN** `porter.infrastructure.fetcher.HttpFetcher` is checked against `HtmlFetcher`
- **THEN** it is recognized as a valid implementation without importing or inheriting from `HtmlFetcher`
