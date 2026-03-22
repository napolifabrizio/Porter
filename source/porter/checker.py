from dataclasses import dataclass

from porter.database import Database
from porter.models import Product
from porter.scraper import Scraper


@dataclass
class CheckResult:
    product: Product
    dropped: bool
    change_pct: float
    error: str | None


class PriceChecker:
    DROP_THRESHOLD = 0.05

    def __init__(self, scraper: Scraper, db: Database):
        self._scraper = scraper
        self._db = db

    def check_all_prices(self, products: list[Product]) -> list[CheckResult]:
        results: list[CheckResult] = []

        for product in products:
            try:
                scraped = self._scraper.fetch_and_scrape(product.url)
                self._db.update_price(product.id, scraped.price)

                change_pct = (product.initial_price - scraped.price) / product.initial_price
                dropped = change_pct >= self.DROP_THRESHOLD

                results.append(CheckResult(
                    product=product,
                    dropped=dropped,
                    change_pct=change_pct,
                    error=None,
                ))
            except Exception as e:
                results.append(CheckResult(
                    product=product,
                    dropped=False,
                    change_pct=0.0,
                    error=str(e),
                ))

        return results
