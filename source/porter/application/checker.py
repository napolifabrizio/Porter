from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass

from porter.application.ports import HtmlFetcher, ProductRepository, ProductScraper
from porter.domain.price_rules import evaluate_price_drop
from porter.models import Product


@dataclass
class CheckResult:
    product: Product
    dropped: bool
    rose: bool
    change_pct: float
    error: str | None
    scraped_by_llm: bool = False


class PriceChecker:
    def __init__(self, scraper: ProductScraper, repo: ProductRepository, fetcher: HtmlFetcher):
        self._scraper = scraper
        self._repo = repo
        self._fetcher = fetcher

    def _check_one(self, product: Product) -> CheckResult:
        try:
            html = self._fetcher.fetch(product.url)
            scraped = self._scraper.scrape(html)
            self._repo.update_price(product.id, scraped.price)
            dropped, rose, change_pct = evaluate_price_drop(product.initial_price, scraped.price)
            return CheckResult(product=product, dropped=dropped, rose=rose, change_pct=change_pct, error=None, scraped_by_llm=scraped.scraped_by_llm)
        except Exception as e:
            return CheckResult(product=product, dropped=False, rose=False, change_pct=0.0, error=str(e), scraped_by_llm=False)

    def check_all_prices(self, products: list[Product]) -> list[CheckResult]:
        with ThreadPoolExecutor(max_workers=min(10, len(products))) as pool:
            futures: dict[Future[CheckResult], int] = {
                pool.submit(self._check_one, product): i
                for i, product in enumerate(products)
            }
            results: list[CheckResult | None] = [None] * len(products)
            for future, index in futures.items():
                results[index] = future.result()
        return results  # type: ignore[return-value]
