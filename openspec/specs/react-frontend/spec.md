## Requirements

### Requirement: React SPA is scaffolded in App/ with Vite and TypeScript
The system SHALL contain a Vite + React + TypeScript project at `App/`. Running `npm run dev` inside `App/` SHALL start the development server. Running `npm run build` SHALL produce a production-ready static bundle in `App/dist/`.

#### Scenario: Dev server starts without errors
- **WHEN** the developer runs `npm run dev` inside `App/`
- **THEN** Vite starts a local development server and the app is accessible in the browser

#### Scenario: Production build succeeds
- **WHEN** the developer runs `npm run build` inside `App/`
- **THEN** Vite produces a `dist/` folder with no TypeScript or build errors

### Requirement: API base URL is configurable via environment variable
The system SHALL read the FastAPI base URL from `VITE_API_URL`. All HTTP calls from the React app SHALL be prefixed with this value. A `.env` file inside `App/` SHALL override the default. The default SHALL be `http://localhost:8000`.

#### Scenario: App uses VITE_API_URL in development
- **WHEN** `VITE_API_URL=http://localhost:8000` is set and the app makes an API call
- **THEN** the request URL begins with `http://localhost:8000`

#### Scenario: App uses VITE_API_URL in production build
- **WHEN** `VITE_API_URL=https://api.example.com` is baked into the production build
- **THEN** every API call in the bundle targets `https://api.example.com`

### Requirement: FastAPI exposes CORS headers for browser clients
The system SHALL configure `CORSMiddleware` on the FastAPI app. In development, `http://localhost:5173` SHALL be an allowed origin. The set of allowed origins SHALL be configurable via a `CORS_ORIGINS` environment variable.

#### Scenario: Browser can reach FastAPI from the Vite dev origin
- **WHEN** the React app on `http://localhost:5173` sends a request to FastAPI on `http://localhost:8000`
- **THEN** FastAPI responds with the appropriate `Access-Control-Allow-Origin` header and the browser does not block the response

#### Scenario: CORS allows configured production origins
- **WHEN** `CORS_ORIGINS=https://porter.example.com` is set and a request arrives from that origin
- **THEN** FastAPI includes `Access-Control-Allow-Origin: https://porter.example.com` in the response

### Requirement: App has client-side routing with /login and /list/:id routes
The system SHALL define two routes: `/login` (unauthenticated entry point) and `/list/$listId` (authenticated main view). Navigating to `/` without auth SHALL redirect to `/login`. Navigating to `/` with auth SHALL redirect to `/list/1` (Standard list).

#### Scenario: Unauthenticated user is redirected to /login
- **WHEN** a user with no JWT in sessionStorage navigates to any route other than `/login`
- **THEN** the app redirects to `/login`

#### Scenario: Authenticated user at root is redirected to default list
- **WHEN** a user with a valid JWT navigates to `/`
- **THEN** the app redirects to `/list/1`

#### Scenario: Navigating to /list/:id renders the correct list
- **WHEN** an authenticated user navigates to `/list/2`
- **THEN** the main view shows products belonging to list 2

### Requirement: Auth guard prevents unauthenticated access to protected routes
The system SHALL wrap all routes except `/login` with an auth guard component. The auth guard SHALL check for a JWT in `sessionStorage` before rendering the route. If no token exists, it SHALL redirect to `/login`.

#### Scenario: Protected route without token redirects
- **WHEN** sessionStorage has no JWT and the user navigates to `/list/1`
- **THEN** the app renders the login page instead of the product list

#### Scenario: Protected route with valid token renders normally
- **WHEN** sessionStorage has a JWT and the user navigates to `/list/1`
- **THEN** the product list is rendered without redirecting

### Requirement: JWT is stored in and restored from sessionStorage
The system SHALL store the JWT returned by `POST /auth/login` in `sessionStorage` under the key `porter_token`. On app load, the system SHALL read this key to restore auth state. Closing the browser tab SHALL clear sessionStorage, requiring the user to log in again.

#### Scenario: Token is saved after successful login
- **WHEN** the user submits the correct password on the login page
- **THEN** the JWT is written to `sessionStorage["porter_token"]` and the user is redirected to `/list/1`

#### Scenario: Token is restored on page reload
- **WHEN** the user reloads the app and `sessionStorage["porter_token"]` exists
- **THEN** the user remains authenticated without re-entering their password

#### Scenario: Token is absent after tab close
- **WHEN** the user closes the browser tab and reopens the app URL
- **THEN** `sessionStorage["porter_token"]` is empty and the user sees the login page

### Requirement: Typed API client sends Bearer token on every authenticated request
The system SHALL provide a single `api/client.ts` module that exports typed async functions for all FastAPI endpoints. Every call to a protected endpoint SHALL include an `Authorization: Bearer <token>` header sourced from the Zustand auth store.

#### Scenario: Authenticated request includes Bearer header
- **WHEN** the user is logged in and any data-fetching hook fires
- **THEN** the outgoing HTTP request contains `Authorization: Bearer <jwt>`

#### Scenario: Unauthenticated request returns 401 and redirects to login
- **WHEN** a request is made with a missing or expired token
- **THEN** the API returns 401 and the app clears the token and redirects to `/login`

### Requirement: Long-running price check operations show a blocking full-page spinner
The system SHALL display a full-page overlay spinner while `POST /products/check` or `POST /products/check-selected` is in-flight. All interactive elements SHALL be non-interactable during this time. The spinner label SHALL describe the operation.

#### Scenario: Full-page spinner appears during check-all
- **WHEN** the user clicks "Check All Prices"
- **THEN** a full-page overlay with a descriptive spinner label is rendered and all buttons are disabled until the response returns

#### Scenario: Full-page spinner appears during check-selected
- **WHEN** the user clicks "Check Selected (N)" with N ≥ 1
- **THEN** a full-page overlay spinner is shown until the selected-check response returns

#### Scenario: UI is restored after check completes
- **WHEN** the price check response is received
- **THEN** the spinner is removed and the product list is re-rendered with updated prices and stripe indicators
