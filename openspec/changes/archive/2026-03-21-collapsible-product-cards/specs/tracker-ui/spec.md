## MODIFIED Requirements

### Requirement: Product list shows price status with visual indicators
The system SHALL display each tracked product as a collapsible card. The collapsed (default) state SHALL show only the product name and current price. The expanded state SHALL additionally show the product description (if present), the product URL, and the initial price. A toggle control in the card header SHALL switch between collapsed and expanded states. The price/status visual indicator (↓ green with percentage, = neutral, or red error) SHALL be visible in both states.

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
