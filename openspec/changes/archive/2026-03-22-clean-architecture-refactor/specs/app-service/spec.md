## MODIFIED Requirements

### Requirement: AppService exposes a unified interface for all UI operations
The system SHALL provide an `AppService` class in `source/porter/application/service.py` that serves as the sole entry point for the UI layer to interact with the backend. `AppService` SHALL instantiate and wire all backend classes internally, using the concrete infrastructure implementations (`Database`, `Scraper`).

#### Scenario: Frontend imports only AppService
- **WHEN** the UI module (`ui/app.py`) needs to perform any backend operation
- **THEN** it imports only `AppService` from `porter.application.service` and no other backend module

#### Scenario: AppService initializes all backend dependencies
- **WHEN** `AppService()` is instantiated
- **THEN** it creates `Database`, `Scraper`, and `PriceChecker` instances internally without requiring them as constructor arguments
