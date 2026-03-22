## ADDED Requirements

### Requirement: Source code is organized into four explicit layers
The system SHALL organize `source/porter/` into four sub-packages: `domain/`, `application/`, `infrastructure/`, and `ui/`. `models.py` SHALL remain at the `source/porter/` root as a shared value-object module available to all layers.

#### Scenario: Layers exist as packages
- **WHEN** the repository is checked out
- **THEN** `source/porter/domain/__init__.py`, `source/porter/application/__init__.py`, `source/porter/infrastructure/__init__.py`, and `source/porter/ui/__init__.py` all exist

### Requirement: Dependency rule — inner layers never import from outer layers
Imports SHALL only flow inward: `ui` may import from `application` and `infrastructure`; `application` may import from `domain`; `domain` SHALL import nothing from other Porter layers. No inner layer SHALL import from an outer layer.

#### Scenario: Domain has no porter imports
- **WHEN** any file under `source/porter/domain/` is statically analyzed
- **THEN** it contains no imports from `porter.application`, `porter.infrastructure`, or `porter.ui`

#### Scenario: Application has no infrastructure imports
- **WHEN** any file under `source/porter/application/` is statically analyzed
- **THEN** it contains no imports from `porter.infrastructure` or `porter.ui`

### Requirement: Domain layer contains only pure business logic
The `domain/` package SHALL contain only code with no I/O, no network, no database, and no framework dependencies. All domain logic SHALL be expressible as pure functions or simple dataclasses.

#### Scenario: Domain has no I/O dependencies
- **WHEN** any file under `source/porter/domain/` is imported in isolation
- **THEN** it does not require `httpx`, `sqlite3`, `langchain`, `openai`, or `streamlit` to be installed
