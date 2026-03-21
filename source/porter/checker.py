from dataclasses import dataclass

from porter.database import update_price
from porter.models import Product
from porter.scraper import fetch_and_scrape

DROP_THRESHOLD = 0.05


@dataclass
class CheckResult:
    product: Product
    dropped: bool
    change_pct: float
    error: str | None


def check_all_prices(products: list[Product]) -> list[CheckResult]:
    results: list[CheckResult] = []

    for product in products:
        try:
            scraped = fetch_and_scrape(product.url)
            update_price(product.id, scraped.price)

            change_pct = (product.initial_price - scraped.price) / product.initial_price
            dropped = change_pct >= DROP_THRESHOLD

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
