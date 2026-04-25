import os
from datetime import datetime, timezone

from sqlalchemy import Integer, String, Float, ForeignKey, create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from porter.models import Product, ScrapedData, WatchList


class _Base(DeclarativeBase):
    pass


class _ListRow(_Base):
    __tablename__ = "lists"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)


class _ProductRow(_Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    initial_price: Mapped[float] = mapped_column(Float, nullable=False)
    current_price: Mapped[float] = mapped_column(Float, nullable=False)
    last_checked: Mapped[str] = mapped_column(String, nullable=False)
    list_id: Mapped[int] = mapped_column(Integer, ForeignKey("lists.id"), nullable=False, default=1)
    currency: Mapped[str] = mapped_column(String, nullable=False, default="R$")


class _AppConfigRow(_Base):
    __tablename__ = "app_config"
    key: Mapped[str] = mapped_column(String, primary_key=True)
    value: Mapped[str] = mapped_column(String, nullable=False)


class Database:
    def __init__(self):
        url = os.environ["DATABASE_URL"]
        self._engine = create_engine(url, connect_args={"client_encoding": "utf8"})
        self._Session = sessionmaker(bind=self._engine)

    # ── Config methods ──────────────────────────────────────────────────────────

    def get_config(self, key: str) -> str | None:
        with self._Session() as session:
            row = session.get(_AppConfigRow, key)
        return row.value if row else None

    def set_config(self, key: str, value: str) -> None:
        with self._Session() as session:
            row = _AppConfigRow(key=key, value=value)
            session.merge(row)
            session.commit()

    # ── WatchList methods ───────────────────────────────────────────────────────

    def create_list(self, name: str) -> WatchList:
        try:
            with self._Session() as session:
                row = _ListRow(name=name)
                session.add(row)
                session.flush()
                list_id = row.id
                session.commit()
        except IntegrityError:
            raise ValueError(f"A list named '{name}' already exists.")
        return WatchList(id=list_id, name=name)

    def list_all_lists(self) -> list[WatchList]:
        with self._Session() as session:
            rows = session.query(_ListRow).order_by(_ListRow.id.asc()).all()
            return [WatchList(id=r.id, name=r.name) for r in rows]

    def delete_list(self, list_id: int) -> None:
        with self._Session() as session:
            session.query(_ProductRow).filter(_ProductRow.list_id == list_id).update(
                {_ProductRow.list_id: 1}
            )
            session.query(_ListRow).filter(_ListRow.id == list_id).delete()
            session.commit()

    def move_product_to_list(self, product_id: int, list_id: int) -> None:
        with self._Session() as session:
            target = session.get(_ListRow, list_id)
            if target is None:
                raise ValueError(f"List with id={list_id} does not exist.")
            session.query(_ProductRow).filter(_ProductRow.id == product_id).update(
                {_ProductRow.list_id: list_id}
            )
            session.commit()

    # ── Product methods ─────────────────────────────────────────────────────────

    def add_product(self, scraped: ScrapedData, url: str, list_id: int | None = None) -> Product:
        effective_list_id = list_id if list_id is not None else 1
        now = datetime.now(timezone.utc).isoformat()
        try:
            with self._Session() as session:
                row = _ProductRow(
                    url=url,
                    name=scraped.name,
                    description=scraped.description,
                    initial_price=scraped.price,
                    current_price=scraped.price,
                    last_checked=now,
                    list_id=effective_list_id,
                    currency=scraped.currency,
                )
                session.add(row)
                session.flush()
                product_id = row.id
                session.commit()
        except IntegrityError:
            raise ValueError(f"Product with URL already tracked: {url}")
        return Product(
            id=product_id,
            url=url,
            name=scraped.name,
            description=scraped.description,
            initial_price=scraped.price,
            current_price=scraped.price,
            last_checked=now,
            list_id=effective_list_id,
            currency=scraped.currency,
        )

    def list_products(self, list_id: int | None = None) -> list[Product]:
        with self._Session() as session:
            q = session.query(_ProductRow).order_by(_ProductRow.id.asc())
            if list_id is not None:
                q = q.filter(_ProductRow.list_id == list_id)
            rows = q.all()
            return [
                Product(
                    id=r.id,
                    url=r.url,
                    name=r.name,
                    description=r.description,
                    initial_price=r.initial_price,
                    current_price=r.current_price,
                    last_checked=r.last_checked.isoformat() if hasattr(r.last_checked, 'isoformat') else r.last_checked,
                    list_id=r.list_id,
                    currency=r.currency,
                )
                for r in rows
            ]

    def update_price(self, product_id: int, new_price: float) -> None:
        now = datetime.now(timezone.utc).isoformat()
        with self._Session() as session:
            session.query(_ProductRow).filter(_ProductRow.id == product_id).update(
                {_ProductRow.current_price: new_price, _ProductRow.last_checked: now}
            )
            session.commit()

    def update_name(self, product_id: int, name: str) -> None:
        with self._Session() as session:
            session.query(_ProductRow).filter(_ProductRow.id == product_id).update(
                {_ProductRow.name: name}
            )
            session.commit()

    def remove_product(self, product_id: int) -> None:
        with self._Session() as session:
            session.query(_ProductRow).filter(_ProductRow.id == product_id).delete()
            session.commit()
