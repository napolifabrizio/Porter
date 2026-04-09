## Requirements

### Requirement: User can create a named list
The system SHALL allow the user to create a named watchlist. List names SHALL be non-empty and unique (case-sensitive). Creating a duplicate name SHALL raise a `ValueError`.

#### Scenario: List created successfully
- **WHEN** the user provides a unique, non-empty name and confirms creation
- **THEN** the new list appears in the sidebar and is immediately available as a target for products

#### Scenario: Duplicate name rejected
- **WHEN** the user attempts to create a list with a name that already exists
- **THEN** the system displays a warning and does not create a duplicate

#### Scenario: Empty name rejected
- **WHEN** the user submits an empty or whitespace-only name
- **THEN** the system displays a validation warning and does not create the list

### Requirement: A Standard list always exists and cannot be deleted
The system SHALL ensure a list named "Standard" with `id = 1` always exists. It SHALL be created automatically on `init_db()` if absent. Any attempt to delete the Standard list SHALL raise a `ValueError`.

#### Scenario: Standard list present on first run
- **WHEN** the application starts for the first time
- **THEN** the Standard list exists in the database and is visible in the sidebar

#### Scenario: Standard list present after restart
- **WHEN** the application restarts against an existing database
- **THEN** the Standard list is still present and unchanged

#### Scenario: Standard list deletion rejected
- **WHEN** the user attempts to delete the Standard list
- **THEN** the system raises an error and the list is not removed

### Requirement: User can delete a non-Standard list
The system SHALL allow the user to delete any list other than Standard. All products belonging to the deleted list SHALL be moved to the Standard list automatically before the list row is removed.

#### Scenario: Products moved to Standard on list delete
- **WHEN** the user deletes a list that contains products
- **THEN** all products from that list are moved to Standard, and no products are lost

#### Scenario: Empty list deleted cleanly
- **WHEN** the user deletes a list that has no products
- **THEN** the list is removed with no side-effects

### Requirement: User can move a product to a different list
The system SHALL allow the user to reassign a product from its current list to any other existing list at any time.

#### Scenario: Product moved to target list
- **WHEN** the user selects a different list for a product and confirms
- **THEN** the product's `list_id` is updated and it no longer appears under the previous list

#### Scenario: Moving to non-existent list rejected
- **WHEN** code attempts to move a product to a list ID that does not exist
- **THEN** the system raises a `ValueError` and the product's list is unchanged

### Requirement: Products are assigned to a list at add-time
The system SHALL require a `list_id` when adding a new product. If no list is specified, the product SHALL default to the Standard list.

#### Scenario: Product added to selected list
- **WHEN** the user adds a product with a specific list selected
- **THEN** the product is stored with the corresponding `list_id`

#### Scenario: Product defaults to Standard when no list selected
- **WHEN** a product is added without specifying a list
- **THEN** the product's `list_id` is set to the Standard list's ID (1)