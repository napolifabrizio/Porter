## Requirements

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

### Requirement: Application is launchable via React dev server
The system SHALL be runnable with `npm run dev` inside `App/` from the project root. On launch, the app SHALL display a login screen before any other content. The full app SHALL only be rendered after successful JWT-based authentication.

#### Scenario: App starts without errors
- **WHEN** the command `npm run dev` is executed inside `App/`
- **THEN** the Vite dev server starts and the React app opens in the browser without console errors or build failures

#### Scenario: Lock screen is the first thing rendered
- **WHEN** the app starts and sessionStorage has no JWT
- **THEN** only the login page is shown; no product data, sidebar, or other UI is rendered

#### Scenario: Successful login redirects to the product view
- **WHEN** the user enters the correct password and submits the login form
- **THEN** the JWT is stored in sessionStorage and the app navigates to `/list/1`

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
