# UI — `source/porter/ui/`

The `ui/` folder is the application's entry point and the only layer that interacts with the user directly. It contains a single file, `app.py`, which is a **Streamlit** web app.

## Responsibilities

- **Add products**: accepts a URL from the user, calls `AppService.track()`, and displays the scraped name and price.
- **List products**: renders every tracked product as a card with its current price and last-check result.
- **Check prices**: triggers `AppService.check_all_prices()` or `AppService.check_selected()` and shows a colored stripe (green = dropped ≥5%, red = risen, blue = unchanged) alongside a percentage badge.
- **Remove products**: deletes a product from the watchlist via `AppService.remove_product()`.
- **LLM badge**: shows a robot icon on cards where the price was obtained through the LLM fallback scraper.
- **API key warning**: alerts the user in the sidebar when `OPENAI_API_KEY` is missing.

## Position in the architecture

`ui/` sits at the outermost layer of the Clean Architecture. It depends only on `application/service.py` (`AppService`) and never touches infrastructure, domain, database and any other backend module ordirectly, it can only see `AppService`. No business logic lives here — it delegates everything to the application layer and only handles rendering and user input.
