## ADDED Requirements

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
