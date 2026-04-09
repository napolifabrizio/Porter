## Context

Porter scrapes product prices and stores them as floats. The current `_normalize_price` method strips all non-numeric characters (including currency symbols) before parsing, discarding currency information entirely. Neither `ScrapedData` nor `Product` carry a `currency` field, and the database has no `currency` column. The UI hardcodes `R$` everywhere.

The fix touches 5 files across 4 layers: scraper (infrastructure), models, database (infrastructure), and UI.

## Goals / Non-Goals

**Goals:**
- Detect the currency symbol from the raw scraped price string
- Persist currency per-product in the database
- Display each product's actual currency symbol in the UI
- Migrate existing rows safely with a BRL default

**Non-Goals:**
- Currency conversion between units
- Automatic re-scraping of existing products to backfill currency
- Support for currencies not represented by a visible symbol in the price string (e.g. bare numeric prices with no symbol)

## Decisions

### 1. Store symbol, not ISO code
Store the display symbol (`$`, `R$`, `€`) directly rather than the ISO code (`USD`, `BRL`, `EUR`).

**Rationale**: The UI needs a symbol for display; ISO codes would require a secondary lookup table. The symbol is available directly from the raw price string. For JSON-LD `priceCurrency` (which yields ISO codes), map to symbol via a small constant dict.

**Alternative considered**: Store ISO code and map at render time — adds indirection with no benefit for this use case.

### 2. Extract currency before normalization, not after
`_extract_currency(raw: str) -> str` runs on the raw price string before `_normalize_price` strips symbols.

**Rationale**: `_normalize_price` intentionally destroys non-numeric characters. The only clean extraction point is before that step.

### 3. JSON-LD `priceCurrency` takes priority
When JSON-LD structured data includes `offers.priceCurrency` (ISO code), use it. Fall back to symbol scanning of `price_raw`.

**Rationale**: Structured data is the most reliable source; symbol scanning is a heuristic.

### 4. Default currency: `R$`
New `ScrapedData` and `Product` fields default to `"R$"`. DB migration adds `currency TEXT NOT NULL DEFAULT 'R$'`.

**Rationale**: Existing products are from Brazilian stores. Defaulting to BRL avoids incorrect display for the majority of existing data without requiring a re-scrape.

### 5. No changes to `update_price`
Currency is fixed at insert time and never changes for a product.

**Rationale**: A product's currency is determined by the store, not the price value. Price updates don't change the store.

## Risks / Trade-offs

- **Existing product 20 (USD) shows R$ after migration** → User must delete and re-add the product. Acceptable given the default decision above and that it's a personal tool.
- **Symbol scanning is a heuristic** → Unrecognized currencies fall back to `"R$"`. For the supported set (`R$`, `$`, `€`, `£`, `¥`) this covers all major use cases.
- **`R$` must be matched before `$`** → Order of symbol checks matters; `"R$".contains("$")` is true. Implementation must check `"R$"` first.

## Migration Plan

1. `database.py` `init_db` already has a migration pattern (the `list_id` column). Add the same pattern for `currency`:
   ```sql
   ALTER TABLE products ADD COLUMN currency TEXT DEFAULT 'R$'
   UPDATE products SET currency = 'R$' WHERE currency IS NULL
   ```
2. No rollback complexity — adding a nullable-defaulted column is non-destructive.

## Open Questions

None — all decisions resolved during exploration.
