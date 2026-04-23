## MODIFIED Requirements

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
