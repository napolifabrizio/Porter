## MODIFIED Requirements

### Requirement: User can add a product by pasting a URL
The system SHALL provide a text input and a list selector dropdown alongside an "Add Product" button. The list selector SHALL be pre-populated with all available lists and SHALL default to the currently active list. When clicked, the system scrapes the URL and saves the product to the selected list.

#### Scenario: Valid URL added to selected list
- **WHEN** the user pastes a valid product URL, selects a list, and clicks "Add Product"
- **THEN** the system scrapes the page, saves the product to the selected list, and displays a success message

#### Scenario: Duplicate URL rejected in UI
- **WHEN** the user attempts to add a URL already in the database
- **THEN** the system displays a warning message and does not add a duplicate

#### Scenario: Scrape failure shown in UI
- **WHEN** the scraper fails to extract product data from the URL
- **THEN** the system displays an error message describing the failure; no product is saved

## ADDED Requirements

### Requirement: Sidebar shows list navigation
The system SHALL display the available watchlists in the sidebar above the "Actions" section. Clicking a list name SHALL filter the main product view to show only that list's products. The currently active list SHALL be visually indicated.

#### Scenario: Lists visible in sidebar
- **WHEN** the user opens the app
- **THEN** the sidebar shows all available lists including Standard

#### Scenario: Clicking a list filters the product view
- **WHEN** the user clicks a list name in the sidebar
- **THEN** only products belonging to that list are shown in the main area

#### Scenario: Active list is visually indicated
- **WHEN** a list is selected
- **THEN** it is visually distinguished from the other lists in the sidebar

### Requirement: User can create and delete lists from the sidebar
The system SHALL provide a control in the sidebar to create a new named list and a delete button next to each non-Standard list.

#### Scenario: New list created from sidebar
- **WHEN** the user enters a name and confirms list creation
- **THEN** the new list appears in the sidebar and is immediately selectable

#### Scenario: Non-Standard list deleted from sidebar
- **WHEN** the user clicks the delete button for a non-Standard list and confirms
- **THEN** the list is removed from the sidebar and its products are moved to Standard

#### Scenario: Standard list has no delete button
- **WHEN** the sidebar is rendered
- **THEN** the Standard list does not show a delete button

### Requirement: Product cards show a move-to-list control
Each product card SHALL include a control (e.g. selectbox) that allows the user to move the product to a different list. Selecting a new list SHALL immediately update the product's assignment and refresh the view.

#### Scenario: Move control shows other lists
- **WHEN** a product card is rendered
- **THEN** the move control displays all lists except the product's current list

#### Scenario: Product moved via card control
- **WHEN** the user selects a different list in the move control
- **THEN** the product is reassigned to the new list and disappears from the current list view

### Requirement: Product list is filtered to the active list
The system SHALL only show products belonging to the currently selected list. An empty-state message SHALL reference the list name when no products are present.

#### Scenario: Products filtered by active list
- **WHEN** the user has selected list "Foods" and the main area renders
- **THEN** only products with list_id matching "Foods" are shown

#### Scenario: Empty state references active list
- **WHEN** the active list has no products
- **THEN** the message reads "No products in [list name]. Paste a URL above to get started."
