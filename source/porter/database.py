import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from porter.models import Product, ScrapedData

DB_PATH = Path("porter.db")


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with _connect() as conn:
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


def add_product(scraped: ScrapedData, url: str) -> Product:
    now = datetime.now(timezone.utc).isoformat()
    try:
        with _connect() as conn:
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


def list_products() -> list[Product]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT * FROM products ORDER BY id ASC"
        ).fetchall()
    return [Product(**dict(row)) for row in rows]


def update_price(product_id: int, new_price: float) -> None:
    now = datetime.now(timezone.utc).isoformat()
    with _connect() as conn:
        conn.execute(
            "UPDATE products SET current_price = ?, last_checked = ? WHERE id = ?",
            (new_price, now, product_id),
        )
