import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from porter.models import Product, ScrapedData, WatchList


class Database:
    def __init__(self, db_path: Path = Path("porter.db")):
        self.db_path = db_path

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def init_db(self) -> None:
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS lists (
                    id   INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE
                )
            """)
            conn.execute(
                "INSERT OR IGNORE INTO lists (id, name) VALUES (1, 'Standard')"
            )
            conn.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id            INTEGER PRIMARY KEY AUTOINCREMENT,
                    url           TEXT NOT NULL UNIQUE,
                    name          TEXT NOT NULL,
                    description   TEXT,
                    initial_price REAL NOT NULL,
                    current_price REAL NOT NULL,
                    last_checked  TEXT NOT NULL,
                    list_id       INTEGER NOT NULL DEFAULT 1 REFERENCES lists(id)
                )
            """)
            # Migration: add list_id to existing databases that lack the column
            columns = {
                row["name"]
                for row in conn.execute("PRAGMA table_info(products)").fetchall()
            }
            if "list_id" not in columns:
                conn.execute(
                    "ALTER TABLE products ADD COLUMN list_id INTEGER DEFAULT 1"
                )
                conn.execute(
                    "UPDATE products SET list_id = 1 WHERE list_id IS NULL"
                )

    # ── WatchList methods ───────────────────────────────────────────────────────

    def create_list(self, name: str) -> WatchList:
        try:
            with self._connect() as conn:
                cur = conn.execute(
                    "INSERT INTO lists (name) VALUES (?)", (name,)
                )
                list_id = cur.lastrowid
        except sqlite3.IntegrityError:
            raise ValueError(f"A list named '{name}' already exists.")
        return WatchList(id=list_id, name=name)

    def list_all_lists(self) -> list[WatchList]:
        with self._connect() as conn:
            rows = conn.execute("SELECT id, name FROM lists ORDER BY id ASC").fetchall()
        return [WatchList(id=row["id"], name=row["name"]) for row in rows]

    def delete_list(self, list_id: int) -> None:
        with self._connect() as conn:
            conn.execute(
                "UPDATE products SET list_id = 1 WHERE list_id = ?", (list_id,)
            )
            conn.execute("DELETE FROM lists WHERE id = ?", (list_id,))

    def move_product_to_list(self, product_id: int, list_id: int) -> None:
        with self._connect() as conn:
            # Verify target list exists
            row = conn.execute(
                "SELECT id FROM lists WHERE id = ?", (list_id,)
            ).fetchone()
            if row is None:
                raise ValueError(f"List with id={list_id} does not exist.")
            conn.execute(
                "UPDATE products SET list_id = ? WHERE id = ?", (list_id, product_id)
            )

    # ── Product methods ─────────────────────────────────────────────────────────

    def add_product(self, scraped: ScrapedData, url: str, list_id: int | None = None) -> Product:
        effective_list_id = list_id if list_id is not None else 1
        now = datetime.now(timezone.utc).isoformat()
        try:
            with self._connect() as conn:
                cur = conn.execute(
                    """
                    INSERT INTO products
                        (url, name, description, initial_price, current_price, last_checked, list_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (url, scraped.name, scraped.description, scraped.price, scraped.price, now, effective_list_id),
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
            list_id=effective_list_id,
        )

    def list_products(self, list_id: int | None = None) -> list[Product]:
        with self._connect() as conn:
            if list_id is None:
                rows = conn.execute(
                    "SELECT * FROM products ORDER BY id ASC"
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM products WHERE list_id = ? ORDER BY id ASC",
                    (list_id,),
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
