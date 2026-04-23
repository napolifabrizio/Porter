import os
from datetime import datetime, timedelta, timezone

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from porter.application.service import AppService
from porter.models import (
    CheckResultResponse,
    CheckSelectedRequest,
    CreateListRequest,
    LoginRequest,
    LoginResponse,
    MoveRequest,
    Product,
    TrackRequest,
    TrackResultResponse,
    WatchList,
)

app = FastAPI(title="Porter API")

_cors_origins = os.environ.get("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_svc = AppService()
_bearer = HTTPBearer()

_SECRET_KEY = os.environ["SECRET_KEY"]
_ALGORITHM = "HS256"
_TOKEN_EXPIRE_DAYS = 30


def _create_token() -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=_TOKEN_EXPIRE_DAYS)
    return jwt.encode({"sub": "porter", "exp": expire}, _SECRET_KEY, algorithm=_ALGORITHM)


def _require_auth(credentials: HTTPAuthorizationCredentials = Depends(_bearer)) -> None:
    try:
        payload = jwt.decode(credentials.credentials, _SECRET_KEY, algorithms=[_ALGORITHM])
        if payload.get("sub") != "porter":
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# ── Auth ────────────────────────────────────────────────────────────────────────

@app.post("/auth/login", response_model=LoginResponse)
def login(body: LoginRequest) -> LoginResponse:
    if not _svc.verify_password(body.password):
        raise HTTPException(status_code=401, detail="Wrong password")
    return LoginResponse(access_token=_create_token())


# ── Lists ───────────────────────────────────────────────────────────────────────

@app.get("/lists", response_model=list[WatchList])
def get_lists(_: None = Depends(_require_auth)) -> list[WatchList]:
    return _svc.list_all_lists()


@app.post("/lists", response_model=WatchList, status_code=201)
def create_list(body: CreateListRequest, _: None = Depends(_require_auth)) -> WatchList:
    try:
        return _svc.create_list(body.name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/lists/{list_id}", status_code=204)
def delete_list(list_id: int, _: None = Depends(_require_auth)) -> None:
    try:
        _svc.delete_list(list_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ── Products ────────────────────────────────────────────────────────────────────

@app.get("/products", response_model=list[Product])
def get_products(list_id: int | None = None, _: None = Depends(_require_auth)) -> list[Product]:
    return _svc.list_products(list_id=list_id)


@app.post("/products", response_model=TrackResultResponse, status_code=201)
def track_product(body: TrackRequest, _: None = Depends(_require_auth)) -> TrackResultResponse:
    try:
        result = _svc.track(body.url, list_id=body.list_id)
        return TrackResultResponse(product=result.product, scraped_by_llm=result.scraped_by_llm)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))


@app.post("/products/check", response_model=list[CheckResultResponse])
def check_all_prices(list_id: int | None = None, _: None = Depends(_require_auth)) -> list[CheckResultResponse]:
    results = _svc.check_all_prices(list_id=list_id)
    return [
        CheckResultResponse(
            product=r.product,
            dropped=r.dropped,
            change_pct=r.change_pct,
            error=r.error,
            scraped_by_llm=r.scraped_by_llm,
        )
        for r in results
    ]


@app.post("/products/check-selected", response_model=list[CheckResultResponse])
def check_selected(body: CheckSelectedRequest, _: None = Depends(_require_auth)) -> list[CheckResultResponse]:
    results = _svc.check_selected(body.ids)
    return [
        CheckResultResponse(
            product=r.product,
            dropped=r.dropped,
            change_pct=r.change_pct,
            error=r.error,
            scraped_by_llm=r.scraped_by_llm,
        )
        for r in results
    ]


@app.delete("/products/{product_id}", status_code=204)
def remove_product(product_id: int, _: None = Depends(_require_auth)) -> None:
    _svc.remove_product(product_id)


@app.patch("/products/{product_id}/list", status_code=204)
def move_product(product_id: int, body: MoveRequest, _: None = Depends(_require_auth)) -> None:
    _svc.move_product(product_id, body.target_list_id)
