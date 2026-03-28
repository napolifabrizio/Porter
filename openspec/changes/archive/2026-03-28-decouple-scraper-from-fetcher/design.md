## Context

`Scraper` currently mixes two concerns: HTTP fetching (via `HtmlFetcher`) and HTML parsing (JSON-LD, BS4, LLM fallback). Both concerns live inside `fetch_and_scrape(url)`. This makes it impossible to test parsing logic without a real HTTP call or a mocked fetcher. The `ProductScraper` protocol reflects this coupling — its method signature exposes a URL, not HTML.

The change pushes fetching responsibility up the call stack: callers (`AppService`, `PriceChecker`) fetch the HTML and hand it to the parser.

## Goals / Non-Goals

**Goals:**
- `Scraper` has no I/O dependency other than the LLM call (which remains)
- Parsing logic can be tested by passing an HTML string directly
- `PriceChecker` stays in the application layer and depends only on protocols

**Non-Goals:**
- Removing the LLM I/O from `Scraper` (out of scope)
- Introducing async fetching or connection pooling
- Adding tests (this change enables testability; writing tests is a separate concern)

## Decisions

### Decision 1: Fetching moves to callers — not a new wrapper class

**Options considered:**
- A) Callers (`AppService`, `PriceChecker`) fetch HTML themselves — chosen
- B) A thin `FetchAndScrape` wrapper holds both fetcher and scraper and satisfies the old protocol

Option A is preferred because Option B just moves the coupling one level up without eliminating it, and introduces a class whose sole job is to glue two others together. Option A is more explicit and makes each caller's dependencies visible at construction time.

### Decision 2: `ProductScraper` protocol changes to `scrape(html: str)`

The protocol must change to match the new `Scraper` signature. This is a breaking change at the protocol level, but since `Scraper` is the only implementation and `PriceChecker` is the only consumer, the blast radius is contained to four files.

### Decision 3: `PriceChecker` receives `HtmlFetcher` via constructor

`PriceChecker` lives in the application layer and must not import `HttpFetcher` directly. Adding `fetcher: HtmlFetcher` to its constructor keeps it depending only on a protocol — consistent with how it already receives `ProductScraper` and `ProductRepository`.

### Decision 4: `AppService` stores the fetcher instance

`AppService` is the composition root. It already wires all dependencies. Adding `self._fetcher = HttpFetcher()` and passing it to both the checker and using it in `track()` is the natural place.

## Risks / Trade-offs

- **Parallel fetch in `PriceChecker`**: `PriceChecker._check_one` already runs in threads. Moving `fetcher.fetch()` inside the thread is fine — `HttpFetcher` makes stateless HTTP calls and `curl_cffi` is thread-safe.
- **`Scraper` still has LLM I/O**: `_scrape_with_llm` calls OpenAI. `Scraper` is not fully pure. This is an accepted trade-off per the proposal's non-goals.
- **Protocol breaking change**: Any external code that depends on `ProductScraper.fetch_and_scrape(url)` would break. Porter has no public API surface, so this is acceptable.
