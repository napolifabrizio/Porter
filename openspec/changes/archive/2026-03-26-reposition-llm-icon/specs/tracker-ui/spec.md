## ADDED Requirements

### Requirement: LLM indicator is shown as a standalone column with tooltip
The system SHALL display a dedicated column between the price/status column and the delete column for the LLM scrape indicator. When a product was scraped via the LLM fallback, the column SHALL show a 🤖 icon with a tooltip reading "This product was scraped via LLM fallback". When a product was not scraped via LLM, the column SHALL be empty. The icon SHALL NOT be embedded in the product name button label.

#### Scenario: LLM-scraped product shows icon in dedicated column
- **WHEN** a product has `scraped_by_llm` equal to true
- **THEN** the 🤖 icon appears in the column between the price and the delete button, with a tooltip reading "This product was scraped via LLM fallback"

#### Scenario: Non-LLM product shows empty icon column
- **WHEN** a product has `scraped_by_llm` equal to false
- **THEN** the icon column is empty and the row layout remains aligned with other rows

#### Scenario: Product name button contains no LLM icon
- **WHEN** any product card is rendered
- **THEN** the product name toggle button label contains only the expand arrow and product name, with no 🤖 character
