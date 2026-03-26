from pydantic import BaseModel


class ScrapedData(BaseModel):
    name: str
    price: float
    description: str | None = None
    scraped_by_llm: bool = False


class Product(BaseModel):
    id: int
    url: str
    name: str
    description: str | None
    initial_price: float
    current_price: float
    last_checked: str
