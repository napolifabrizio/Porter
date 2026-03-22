from dataclasses import dataclass

from porter.application.ports import ProductRepository, ProductScraper
from porter.domain.price_rules import evaluate_price_drop
from porter.models import Product


@dataclass
class CheckResult:
    product: Product
    dropped: bool
    change_pct: float
    error: str | None


class PriceChecker:
    def __init__(self, scraper: ProductScraper, repo: ProductRepository):
        self._scraper = scraper
        self._repo = repo

    def check_all_prices(self, products: list[Product]) -> list[CheckResult]:
        results: list[CheckResult] = []

        for product in products:
            try:
                scraped = self._scraper.fetch_and_scrape(product.url)
                self._repo.update_price(product.id, scraped.price)

                dropped, change_pct = evaluate_price_drop(product.initial_price, scraped.price)

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
