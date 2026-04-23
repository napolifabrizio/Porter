## 1. Backend — CORS Middleware

- [x] 1.1 Add `python-jose` is already installed; install `fastapi` CORS dependency (already bundled) — no new deps needed
- [x] 1.2 Add `CORSMiddleware` to `source/porter/app.py` with `CORS_ORIGINS` env var (default `http://localhost:5173`)
- [x] 1.3 Document `CORS_ORIGINS` in `.env.example`

## 2. Scaffold React App

- [x] 2.1 Run `npm create vite@latest App -- --template react-ts` inside the project root
- [x] 2.2 Install core dependencies: `@tanstack/react-query`, `@tanstack/react-router`, `zustand`
- [x] 2.3 Install and configure Tailwind CSS v4 inside `App/`
- [x] 2.4 Install shadcn/ui CLI and init (`npx shadcn@latest init`) — choose Tailwind config
- [x] 2.5 Add shadcn components used by the app: `button`, `input`, `dialog`, `checkbox`, `select`, `badge`
- [x] 2.6 Create `App/.env` with `VITE_API_URL=http://localhost:8000` and document in `.env.example`

## 3. TypeScript Types & API Client

- [x] 3.1 Create `App/src/types.ts` mirroring all Pydantic models (`WatchList`, `Product`, `TrackResultResponse`, `CheckResultResponse`, etc.)
- [x] 3.2 Create `App/src/api/client.ts` with typed async functions for all 10 endpoints (`login`, `getLists`, `createList`, `deleteList`, `getProducts`, `trackProduct`, `checkAllPrices`, `checkSelected`, `deleteProduct`, `moveProduct`)
- [x] 3.3 Wire `VITE_API_URL` as the base URL in the client
- [x] 3.4 Implement `Authorization: Bearer <token>` header injection from the Zustand store
- [x] 3.5 Handle 401 responses globally: clear token and redirect to `/login`

## 4. Auth State (Zustand)

- [x] 4.1 Create `App/src/store/auth.ts` with Zustand store: `{ token, setToken, clearToken }`
- [x] 4.2 Initialize the store by reading `sessionStorage["porter_token"]` on module load
- [x] 4.3 `setToken` SHALL write to both Zustand state and `sessionStorage["porter_token"]`
- [x] 4.4 `clearToken` SHALL clear both Zustand state and `sessionStorage["porter_token"]`

## 5. Routing & Auth Guard

- [x] 5.1 Define TanStack Router route tree with three routes: `/login`, `/` (redirect), `/list/$listId`
- [x] 5.2 Create `beforeLoad` guard on `/list/$listId` that checks for a token; redirect to `/login` if absent
- [x] 5.3 Create an index route at `/` that redirects authenticated users to `/list/1` and unauthenticated users to `/login`
- [x] 5.4 Wrap the app in `RouterProvider` and `QueryClientProvider`

## 6. Login Page

- [x] 6.1 Create `App/src/pages/LoginPage.tsx` with a password input and submit button
- [x] 6.2 Call `POST /auth/login` on submit; on success store the token and navigate to `/list/1`
- [x] 6.3 Show an inline error message on 401 (wrong password)
- [x] 6.4 Show a loading state on the button while the request is in-flight

## 7. API Data Hooks

- [x] 7.1 Create `useLists` hook (`useQuery` on `GET /lists`)
- [x] 7.2 Create `useProducts(listId)` hook (`useQuery` on `GET /products?list_id=`)
- [x] 7.3 Create `useCreateList` mutation
- [x] 7.4 Create `useDeleteList` mutation (invalidates lists + products queries)
- [x] 7.5 Create `useTrackProduct` mutation (invalidates products query)
- [x] 7.6 Create `useCheckAllPrices(listId)` mutation
- [x] 7.7 Create `useCheckSelected` mutation
- [x] 7.8 Create `useDeleteProduct` mutation (invalidates products query)
- [x] 7.9 Create `useMoveProduct` mutation (invalidates products query)

## 8. Sidebar Component

- [x] 8.1 Create `App/src/components/Sidebar.tsx`
- [x] 8.2 Render all lists from `useLists`; highlight the active list based on route param `$listId`
- [x] 8.3 Clicking a list navigates to `/list/$listId`
- [x] 8.4 Render a delete button (🗑) next to non-Standard lists (id ≠ 1)
- [x] 8.5 Delete button opens an inline confirmation dialog; confirm calls `useDeleteList` and navigates to `/list/1` if the deleted list was active
- [x] 8.6 Render a "New List" collapsible form with a text input and create button; calls `useCreateList`
- [x] 8.7 Render "Check All Prices" button and "Check Selected (N)" button in the Actions section

## 9. Add Product Form

- [x] 9.1 Create `App/src/components/AddProductForm.tsx` with a URL text input, list selectbox (pre-selected to current list), and "Add Product" button
- [x] 9.2 On submit call `useTrackProduct`; show a loading spinner inside the button while in-flight
- [x] 9.3 Show a success toast/message with product name and price on success
- [x] 9.4 Show an error message on failure (ValueError → 400, RuntimeError → 502)

## 10. Product Card Component

- [x] 10.1 Create `App/src/components/ProductCard.tsx` accepting a `Product`, optional `CheckResult`, `isSelected`, and callbacks
- [x] 10.2 Render a selection checkbox (always visible, collapsed or expanded)
- [x] 10.3 Render a toggle button with `▶`/`▼` prefix and product name; clicking toggles expand state (local `useState`)
- [x] 10.4 Render a price/status column: green `↓ -X%` for drop, red `↑ +X%` for rise, neutral price otherwise; show red error text on check error
- [x] 10.5 Render a colored left stripe inside the card border (green for drop, red for error, none otherwise)
- [x] 10.6 Render a 🤖 icon column with tooltip "This product was scraped via LLM fallback" when `scraped_by_llm` is true; empty column otherwise
- [x] 10.7 Render a delete button (🗑) that calls `useDeleteProduct` on click
- [x] 10.8 In the expanded state, render: description (truncated to 160 chars), product URL, initial price
- [x] 10.9 Render a "Move to" selectbox (shows all lists except the product's current list); selecting a value calls `useMoveProduct` and resets the selectbox to the placeholder

## 11. Product List & Check Logic

- [x] 11.1 Create `App/src/pages/ListPage.tsx` that composes Sidebar, AddProductForm, and the product list
- [x] 11.2 Render `ProductCard` for each product from `useProducts(listId)`
- [x] 11.3 Maintain `checkResults: Map<productId, CheckResultResponse>` in component state; reset on route change
- [x] 11.4 Maintain `llmScraped: Map<productId, boolean>` in component state; merge in after track or check
- [x] 11.5 Maintain `selectedIds: Set<number>` from checkbox state; pass count to "Check Selected (N)" button
- [x] 11.6 "Check All Prices" button calls `useCheckAllPrices`; on success merge results into `checkResults` and `llmScraped`
- [x] 11.7 "Check Selected" button calls `useCheckSelected` with current `selectedIds`; guards against empty selection with a warning
- [x] 11.8 While any check mutation is in-flight, render a full-page overlay spinner with a descriptive label

## 12. Full-Page Spinner Overlay

- [x] 12.1 Create `App/src/components/CheckingOverlay.tsx` — a fixed full-screen semi-transparent overlay with a centered spinner and label
- [x] 12.2 Render overlay from `ListPage` when `isCheckingAll || isCheckingSelected`
- [x] 12.3 Overlay SHALL prevent pointer events on all underlying UI while visible

## 13. Verification

- [x] 13.1 Run `npm run build` inside `App/` and confirm zero TypeScript errors
- [ ] 13.2 Start FastAPI (`uvicorn porter.app:app`) and the React dev server (`npm run dev`) side-by-side and verify login works end-to-end
- [ ] 13.3 Add a product URL and confirm it appears in the list with correct price
- [ ] 13.4 Check all prices and confirm stripe colors appear correctly
- [ ] 13.5 Create a new list, move a product to it, navigate to it, and delete it — confirm product moves back to Standard
- [ ] 13.6 Verify the 🤖 badge appears for a product that required LLM fallback
- [ ] 13.7 Close the browser tab and reopen — confirm the login page is shown (sessionStorage cleared)
