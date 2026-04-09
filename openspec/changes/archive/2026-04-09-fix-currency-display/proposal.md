## Why

Products from non-BRL storefronts (e.g. Amazon US) have their currency symbol stripped during price normalization and never stored, causing the UI to hardcode "R$" for every product regardless of actual currency.

## What Changes

- Extract and preserve the currency symbol from raw price strings during scraping
- Store currency per-product in the database (new column with BRL default + migration)
- Propagate currency through `ScrapedData` and `Product` models
- Replace all hardcoded "R$" in the UI with the product's actual currency symbol

## Capabilities

### New Capabilities
- `currency-detection`: Detect and persist per-product currency symbol from scraped price data, and display it correctly in the UI

### Modified Capabilities
- `product-scraping`: Scraper must now extract the currency symbol alongside the numeric price
- `product-storage`: Products table gains a `currency` column; `ScrapedData` and `Product` models gain a `currency` field

## Impact

- `source/porter/models.py` — `ScrapedData` and `Product` gain `currency: str`
- `source/porter/infrastructure/scraper.py` — new `_extract_currency` logic; JSON-LD path also reads `priceCurrency`
- `source/porter/infrastructure/database.py` — new `currency` column, migration, INSERT/SELECT changes
- `source/porter/ui/app.py` — all hardcoded `R$` / `R&#36;` replaced with `product.currency`
- No external API or dependency changes
