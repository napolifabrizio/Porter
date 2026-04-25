from pydantic import BaseModel


class ScrapedData(BaseModel):
    name: str
    price: float
    description: str | None = None
    scraped_by_llm: bool = False
    currency: str = "R$"


class WatchList(BaseModel):
    id: int
    name: str


class Product(BaseModel):
    id: int
    url: str
    name: str
    description: str | None
    initial_price: float
    current_price: float
    last_checked: str
    list_id: int = 1
    currency: str = "R$"


# ── API schemas ─────────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    password: str


class LoginResponse(BaseModel):
    access_token: str


class CreateListRequest(BaseModel):
    name: str


class TrackRequest(BaseModel):
    url: str
    list_id: int | None = None


class MoveRequest(BaseModel):
    target_list_id: int


class CheckSelectedRequest(BaseModel):
    ids: list[int]


class TrackResultResponse(BaseModel):
    product: Product
    scraped_by_llm: bool


class CheckResultResponse(BaseModel):
    product: Product
    dropped: bool
    rose: bool
    change_pct: float
    error: str | None
    scraped_by_llm: bool
