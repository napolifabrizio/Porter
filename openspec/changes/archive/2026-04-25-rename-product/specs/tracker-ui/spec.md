## MODIFIED Requirements

### Requirement: Product list shows price status with visual indicators
The system SHALL display each tracked product as a collapsible card. The collapsed (default) state SHALL show only the product name and current price. The expanded state SHALL additionally show the product description (if present), the product URL, and the initial price. A toggle control in the card header SHALL switch between collapsed and expanded states. The price/status visual indicator (↓ green with percentage, = neutral, or red error) SHALL be visible in both states.

The product name in the card header SHALL be inline-editable. Clicking the name text SHALL switch it into an edit input pre-filled with the current name. Pressing Enter or blurring the input SHALL save the change; pressing Escape SHALL cancel and revert to the original name. An empty name SHALL not be saved.

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

#### Scenario: Clicking name enters edit mode
- **WHEN** the user clicks the product name text in the card header
- **THEN** the name is replaced by an editable input pre-filled with the current name

#### Scenario: Enter saves the new name
- **WHEN** the user types a new name in the edit input and presses Enter
- **THEN** the name is saved via API and the card returns to display mode showing the new name

#### Scenario: Blur saves the new name
- **WHEN** the user types a new name in the edit input and clicks outside the input
- **THEN** the name is saved via API and the card returns to display mode showing the new name

#### Scenario: Escape cancels the edit
- **WHEN** the user is editing the name and presses Escape
- **THEN** the input is dismissed and the original name is restored without any API call

#### Scenario: Empty name is not saved
- **WHEN** the user clears the name input and presses Enter or blurs
- **THEN** no API call is made and the original name is restored
