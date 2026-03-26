## ADDED Requirements

### Requirement: User can add a product by pasting a URL
The system SHALL provide a text input and an "Add Product" button. When clicked, the system scrapes the URL and saves the product to the database.

#### Scenario: Valid URL added successfully
- **WHEN** the user pastes a valid product URL and clicks "Add Product"
- **THEN** the system scrapes the page, saves the product, and displays it in the product list with a success message

#### Scenario: Duplicate URL rejected in UI
- **WHEN** the user attempts to add a URL already in the database
- **THEN** the system displays a warning message and does not add a duplicate

#### Scenario: Scrape failure shown in UI
- **WHEN** the scraper fails to extract product data from the URL
- **THEN** the system displays an error message describing the failure; no product is saved

### Requirement: User can trigger a price check for all products
The system SHALL provide a "Check All Prices" button that re-scrapes every tracked product and refreshes the displayed prices.

#### Scenario: Check updates the product list
- **WHEN** the user clicks "Check All Prices"
- **THEN** prices in the list are updated to reflect the latest scraped values

#### Scenario: No products tracked shows empty state
- **WHEN** the user clicks "Check All Prices" and no products are tracked
- **THEN** the system shows an informational message that no products are being tracked

### Requirement: Product list shows price status with visual indicators
The system SHALL display each tracked product as a collapsible card. The collapsed (default) state SHALL show only the product name and current price. The expanded state SHALL additionally show the product description (if present), the product URL, and the initial price. A toggle control in the card header SHALL switch between collapsed and expanded states. The price/status visual indicator (↓ green with percentage, = neutral, or red error) SHALL be visible in both states.

After a price check (all or selected), each product card that participated in the check SHALL display a colored left stripe inside its border to indicate the check result. The stripe color SHALL be green for a price drop ≥ 5%, blue for a stable price, and red for a check error. Products not included in the last check SHALL show no stripe. Stripes SHALL persist across reruns (e.g., expanding a card, toggling a checkbox) until the next check run replaces them. Each new check SHALL replace all previous stripe state — only the most recent check's products are highlighted.

#### Scenario: Dropped product shows green indicator
- **WHEN** a product's price dropped ≥ 5% from initial
- **THEN** the product row shows a green "↓ -X%" label alongside the current price

#### Scenario: Unchanged product shows neutral indicator
- **WHEN** a product's price did not drop ≥ 5% from initial
- **THEN** the product row shows a neutral "=" label

#### Scenario: Failed check shows error per product
- **WHEN** a product's price check failed
- **THEN** the product row shows a red error indicator with the failure message

#### Scenario: Card is collapsed by default
- **WHEN** the product list is rendered
- **THEN** each product card is collapsed, showing only name and current price

#### Scenario: Card expands on toggle click
- **WHEN** the user clicks the toggle control on a collapsed card
- **THEN** the card expands to show description, URL, and initial price

#### Scenario: Card collapses on toggle click when open
- **WHEN** the user clicks the toggle control on an expanded card
- **THEN** the card collapses back to showing only name and current price

### Requirement: Application is launchable via Streamlit
The system SHALL be runnable with `streamlit run source/porter/app.py` from the project root.

#### Scenario: App starts without errors
- **WHEN** the command `streamlit run source/porter/app.py` is executed
- **THEN** the Streamlit app opens in the browser without import errors or crashes

### Requirement: User can select individual products and check only their prices
The system SHALL display a checkbox on each product card that is visible in both collapsed and expanded states, and a "Check Selected (N)" button that, when clicked, re-scrapes and updates only the checked products.

#### Scenario: Check Selected runs only for checked products
- **WHEN** the user checks one or more product checkboxes and clicks "Check Selected"
- **THEN** the system re-scrapes only the selected products and updates their prices in the list

#### Scenario: Check Selected with no products selected shows warning
- **WHEN** the user clicks "Check Selected" with no checkboxes checked
- **THEN** the system displays a warning message and does not trigger any scraping

#### Scenario: Button label reflects selection count
- **WHEN** the user checks N products
- **THEN** the "Check Selected" button label shows "Check Selected (N)"

#### Scenario: Checkbox visible when card is collapsed
- **WHEN** a product card is in the collapsed state
- **THEN** the selection checkbox is still visible and interactive

#### Scenario: Checked product shows colored left stripe
- **WHEN** a price check completes and a product was included in the check
- **THEN** a colored left stripe is displayed inside the product card border (green for drop, blue for stable, red for error)

#### Scenario: Unchecked product shows no stripe
- **WHEN** a price check completes and a product was NOT included in the check
- **THEN** the product card shows no left stripe

#### Scenario: Stripe persists after card interaction
- **WHEN** the user expands or collapses a checked product's card after a check
- **THEN** the colored stripe is still visible on that card

#### Scenario: New check replaces previous stripe state
- **WHEN** the user runs a second check on a different set of products
- **THEN** only the newly checked products show stripes; previously highlighted products show no stripe

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
