## ADDED Requirements

### Requirement: Price check action bar is displayed above the product list
The system SHALL display a price check action bar in the main content area, positioned below the URL input form and above the product list. The action bar SHALL contain both "Check All Prices" and "Check Selected (N)" buttons. The buttons SHALL be disabled while a check is in progress. "Check Selected" SHALL be disabled when no products are selected.

#### Scenario: Action bar is visible in the main content area
- **WHEN** the user navigates to any list page
- **THEN** the "Check All Prices" and "Check Selected (N)" buttons appear between the URL input form and the product list

#### Scenario: Both buttons disabled during a check
- **WHEN** a price check is in progress
- **THEN** both "Check All Prices" and "Check Selected" buttons are disabled

#### Scenario: Check Selected disabled with no selection
- **WHEN** no product checkboxes are checked
- **THEN** the "Check Selected (N)" button is disabled

## MODIFIED Requirements

### Requirement: Sidebar shows list navigation
The system SHALL display the available watchlists in the sidebar. Clicking a list name SHALL filter the main product view to show only that list's products. The currently active list SHALL be visually indicated.

#### Scenario: Lists visible in sidebar
- **WHEN** the user opens the app
- **THEN** the sidebar shows all available lists including Standard

#### Scenario: Clicking a list filters the product view
- **WHEN** the user clicks a list name in the sidebar
- **THEN** only products belonging to that list are shown in the main area

#### Scenario: Active list is visually indicated
- **WHEN** a list is selected
- **THEN** it is visually distinguished from the other lists in the sidebar
