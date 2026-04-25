## ADDED Requirements

### Requirement: Product name is updatable via API
The system SHALL expose a `PATCH /products/{id}` endpoint that accepts a JSON body with a `name` field and updates the product's name in the database. The endpoint SHALL return `400` if `name` is blank or missing, and `404` if the product does not exist.

#### Scenario: Valid rename succeeds
- **WHEN** a `PATCH /products/1` request is sent with `{ "name": "New Name" }`
- **THEN** the system updates the product's name and returns `200` with the updated product

#### Scenario: Blank name rejected
- **WHEN** a `PATCH /products/1` request is sent with `{ "name": "" }`
- **THEN** the system returns `400` without modifying the product

#### Scenario: Unknown product returns 404
- **WHEN** a `PATCH /products/999` request is sent for a non-existent product
- **THEN** the system returns `404`
