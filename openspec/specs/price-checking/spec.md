## ADDED Requirements

### Requirement: Price check re-scrapes all tracked products
The system SHALL re-scrape the current price for every product in the database when a price check is triggered and update `current_price` and `last_checked` for each.

#### Scenario: All products updated on check
- **WHEN** the user triggers a price check and all products scrape successfully
- **THEN** `current_price` and `last_checked` are updated for every product

#### Scenario: Failed scrape does not abort remaining checks
- **WHEN** scraping one product fails during a price check
- **THEN** the system records the error for that product, continues checking remaining products, and reports which products failed at the end

### Requirement: A price drop is detected when current price is ≥ 5% below initial price
The system SHALL flag a product as "price dropped" when `(initial_price − current_price) / initial_price ≥ 0.05`.

#### Scenario: Drop of exactly 5% is flagged
- **WHEN** `initial_price` is `100.00` and `current_price` is `95.00`
- **THEN** the product is flagged as dropped

#### Scenario: Drop below 5% is not flagged
- **WHEN** `initial_price` is `100.00` and `current_price` is `96.00`
- **THEN** the product is NOT flagged as dropped

#### Scenario: Price increase is not flagged
- **WHEN** `current_price` is greater than `initial_price`
- **THEN** the product is NOT flagged as dropped

### Requirement: Check results include per-product status
The system SHALL return a result for each product containing: the product record, whether it dropped, the percentage change, and any error message if the check failed.

#### Scenario: Successful check result
- **WHEN** a product's price was successfully re-scraped
- **THEN** the result includes `dropped: bool`, `change_pct: float`, and `error: None`

#### Scenario: Failed check result
- **WHEN** a product's price could not be scraped
- **THEN** the result includes `error: str` describing the failure and `dropped: False`
