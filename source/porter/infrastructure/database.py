import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from porter.models import Product, ScrapedData


class Database:
    def __init__(self, db_path: Path = Path("porter.db")):
        self.db_path = db_path

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self) -> None:
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id            INTEGER PRIMARY KEY AUTOINCREMENT,
                    url           TEXT NOT NULL UNIQUE,
                    name          TEXT NOT NULL,
                    description   TEXT,
                    initial_price REAL NOT NULL,
                    current_price REAL NOT NULL,
                    last_checked  TEXT NOT NULL
                )
            """)

    def add_product(self, scraped: ScrapedData, url: str) -> Product:
        now = datetime.now(timezone.utc).isoformat()
        try:
            with self._connect() as conn:
                cur = conn.execute(
                    """
                    INSERT INTO products (url, name, description, initial_price, current_price, last_checked)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (url, scraped.name, scraped.description, scraped.price, scraped.price, now),
                )
                product_id = cur.lastrowid
        except sqlite3.IntegrityError:
            raise ValueError(f"Product with URL already tracked: {url}")

        return Product(
            id=product_id,
            url=url,
            name=scraped.name,
            description=scraped.description,
            initial_price=scraped.price,
            current_price=scraped.price,
            last_checked=now,
        )

    def list_products(self) -> list[Product]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM products ORDER BY id ASC"
            ).fetchall()
        return [Product(**dict(row)) for row in rows]

    def update_price(self, product_id: int, new_price: float) -> None:
        now = datetime.now(timezone.utc).isoformat()
        with self._connect() as conn:
            conn.execute(
                "UPDATE products SET current_price = ?, last_checked = ? WHERE id = ?",
                (new_price, now, product_id),
            )

    def remove_product(self, product_id: int) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
