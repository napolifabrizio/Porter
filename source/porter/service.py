from porter.checker import CheckResult, PriceChecker
from porter.database import Database
from porter.models import Product
from porter.scraper import Scraper


class AppService:
    def __init__(self):
        self._db = Database()
        self._scraper = Scraper()
        self._checker = PriceChecker(self._scraper, self._db)
        self._db.init_db()

    def track(self, url: str) -> Product:
        scraped = self._scraper.fetch_and_scrape(url)
        return self._db.add_product(scraped, url)

    def list_products(self) -> list[Product]:
        return self._db.list_products()

    def check_all_prices(self) -> list[CheckResult]:
        products = self._db.list_products()
        return self._checker.check_all_prices(products)

    def check_selected(self, ids: list[int]) -> list[CheckResult]:
        products = [p for p in self._db.list_products() if p.id in ids]
        return self._checker.check_all_prices(products)
