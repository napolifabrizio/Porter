## 1. Models

- [x] 1.1 Add `currency: str = "R$"` field to `ScrapedData` in `models.py`
- [x] 1.2 Add `currency: str = "R$"` field to `Product` in `models.py`

## 2. Scraper — Currency Extraction

- [x] 2.1 Add `_ISO_TO_SYMBOL` constant dict mapping ISO codes to display symbols (`BRL`→`R$`, `USD`→`$`, `EUR`→`€`, `GBP`→`£`, `JPY`→`¥`)
- [x] 2.2 Add `_extract_currency(raw: str) -> str` static method that checks symbols in priority order (`R$` before `$`) and defaults to `"R$"`
- [x] 2.3 Update `_scrape_with_json_ld` to read `offers.priceCurrency`, map via `_ISO_TO_SYMBOL`, and include `currency` in returned `ScrapedData`
- [x] 2.4 Update `_scrape_with_bs4` to call `_extract_currency(price_raw)` and include `currency` in returned `ScrapedData`
- [x] 2.5 Update `_scrape_with_llm` to call `_extract_currency(result.price_raw)` and include `currency` in returned `ScrapedData`

## 3. Database

- [x] 3.1 Add `currency TEXT NOT NULL DEFAULT 'R$'` to the `CREATE TABLE products` statement in `init_db`
- [x] 3.2 Add migration block for `currency` column (following the existing `list_id` migration pattern)
- [x] 3.3 Update `add_product` INSERT statement to include `currency` and pass `scraped.currency`
- [x] 3.4 Update `add_product` `Product(...)` return to pass `currency=scraped.currency`

## 4. UI

- [x] 4.1 Replace hardcoded `R$ {product.current_price:.2f}` and `R&#36; {product.current_price:.2f}` with `{product.currency} {product.current_price:.2f}` in all price display locations (lines 125, 209, 213, 217, 222, 226, 245)
- [x] 4.2 Replace hardcoded `R$ {product.initial_price:.2f}` in the expanded detail section with `{product.currency} {product.initial_price:.2f}`
