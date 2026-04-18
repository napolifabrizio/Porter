## MODIFIED Requirements

### Requirement: Application is launchable via Streamlit
The system SHALL be runnable with `streamlit run source/porter/ui/app.py` from the project root. On launch, the app SHALL display a lock screen before any other content. The full app SHALL only be rendered after successful authentication.

#### Scenario: App starts without errors
- **WHEN** the command `streamlit run source/porter/ui/app.py` is executed
- **THEN** the Streamlit app opens in the browser without import errors or crashes

#### Scenario: Lock screen is the first thing rendered
- **WHEN** the app starts and the session is not authenticated
- **THEN** only the lock screen is shown; no product data, sidebar, or other UI is rendered
