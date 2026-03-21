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
The system SHALL display each tracked product with its name, current price, and a visual indicator: ↓ (green, with percentage) if the price dropped ≥ 5%, or = (neutral) otherwise.

#### Scenario: Dropped product shows green indicator
- **WHEN** a product's price dropped ≥ 5% from initial
- **THEN** the product row shows a green "↓ -X%" label alongside the current price

#### Scenario: Unchanged product shows neutral indicator
- **WHEN** a product's price did not drop ≥ 5% from initial
- **THEN** the product row shows a neutral "=" label

#### Scenario: Failed check shows error per product
- **WHEN** a product's price check failed
- **THEN** the product row shows a red error indicator with the failure message

### Requirement: Application is launchable via Streamlit
The system SHALL be runnable with `streamlit run source/porter/app.py` from the project root.

#### Scenario: App starts without errors
- **WHEN** the command `streamlit run source/porter/app.py` is executed
- **THEN** the Streamlit app opens in the browser without import errors or crashes

### Requirement: User can select individual products and check only their prices
The system SHALL display a checkbox on each product card and a "Check Selected (N)" button that, when clicked, re-scrapes and updates only the checked products.

#### Scenario: Check Selected runs only for checked products
- **WHEN** the user checks one or more product checkboxes and clicks "Check Selected"
- **THEN** the system re-scrapes only the selected products and updates their prices in the list

#### Scenario: Check Selected with no products selected shows warning
- **WHEN** the user clicks "Check Selected" with no checkboxes checked
- **THEN** the system displays a warning message and does not trigger any scraping

#### Scenario: Button label reflects selection count
- **WHEN** the user checks N products
- **THEN** the "Check Selected" button label shows "Check Selected (N)"
