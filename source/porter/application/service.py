from porter.application.checker import CheckResult, PriceChecker
from porter.infrastructure.database import Database
from porter.infrastructure.scraper import Scraper
from porter.models import Product


class AppService:
    def __init__(self):
        self._db = Database()
        self._scraper = Scraper()
        self._checker = PriceChecker(self._scraper, self._db)
        self._products = None
        self._db.init_db()

    def track(self, url: str) -> Product:
        scraped = self._scraper.fetch_and_scrape(url)
        product = self._db.add_product(scraped, url)
        self._populate_or_update_products(True)
        return product

    def list_products(self) -> list[Product]:
        products = self._db.list_products()
        self._products = products
        return products

    def check_all_prices(self) -> list[CheckResult]:
        products = self._populate_or_update_products()
        return self._checker.check_all_prices(products)

    def check_selected(self, ids: list[int]) -> list[CheckResult]:
        products = self._populate_or_update_products()
        products = [p for p in products if p.id in ids]
        return self._checker.check_all_prices(products)

    def _populate_or_update_products(self, update: bool = False) -> list[Product]:
        if self._products is None or update:
            self._products = self._db.list_products()
        return self._products
