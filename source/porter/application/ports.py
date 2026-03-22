from typing import Protocol

from porter.models import Product, ScrapedData


class HtmlFetcher(Protocol):
    def fetch(self, url: str) -> str: ...


class ProductScraper(Protocol):
    def fetch_and_scrape(self, url: str) -> ScrapedData: ...


class ProductRepository(Protocol):
    def init_db(self) -> None: ...

    def add_product(self, scraped: ScrapedData, url: str) -> Product: ...

    def list_products(self) -> list[Product]: ...

    def update_price(self, product_id: int, new_price: float) -> None: ...
