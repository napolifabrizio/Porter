## Requirements

### Requirement: Currency symbol is extracted from raw price strings
The system SHALL extract a currency display symbol from the raw price string before numeric normalization. The extraction SHALL check for known symbols in priority order: `"R$"` before `"$"` to avoid false matching. Supported symbols: `R$`, `$`, `€`, `£`, `¥`. When no symbol is found the system SHALL default to `"R$"`.

#### Scenario: Brazilian Real detected
- **WHEN** the raw price string contains `"R$"` (e.g. `"R$ 1.299,99"`)
- **THEN** the extracted currency symbol is `"R$"`

#### Scenario: US Dollar detected
- **WHEN** the raw price string contains `"$"` but not `"R$"` (e.g. `"$12.99"`)
- **THEN** the extracted currency symbol is `"$"`

#### Scenario: Euro detected
- **WHEN** the raw price string contains `"€"` (e.g. `"€1,299.00"`)
- **THEN** the extracted currency symbol is `"€"`

#### Scenario: Unknown symbol defaults to BRL
- **WHEN** the raw price string contains no recognized currency symbol (e.g. `"1299.99"`)
- **THEN** the extracted currency symbol defaults to `"R$"`

### Requirement: JSON-LD priceCurrency takes priority over symbol scanning
When JSON-LD structured data provides `offers.priceCurrency` as an ISO 4217 code, the system SHALL map it to the corresponding display symbol instead of scanning the raw price string.

Supported mappings: `BRL` → `R$`, `USD` → `$`, `EUR` → `€`, `GBP` → `£`, `JPY` → `¥`.

#### Scenario: ISO code mapped to symbol
- **WHEN** JSON-LD offers contains `"priceCurrency": "USD"`
- **THEN** the product's currency is set to `"$"` without scanning the price string

#### Scenario: Unknown ISO code falls back to symbol scan
- **WHEN** JSON-LD offers contains a `priceCurrency` value not in the mapping table
- **THEN** the system falls back to scanning the raw price string for a recognized symbol

### Requirement: UI displays each product's currency symbol
The system SHALL display the currency symbol stored on each product record in all price fields in the UI. No hardcoded currency string SHALL appear in the product list rendering.

#### Scenario: BRL product displays R$
- **WHEN** a product has `currency = "R$"` and is rendered in the UI
- **THEN** the price is displayed as `"R$ 1.299,99"` style formatting

#### Scenario: USD product displays $
- **WHEN** a product has `currency = "$"` and is rendered in the UI
- **THEN** the price is displayed with `"$"` prefix, not `"R$"`
