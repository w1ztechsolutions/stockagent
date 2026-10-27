"""Read-only database layer for Phungu Insights.

Owns the schema and connection pool.  All mutations happen through
``write_tool`` helpers so the database stays out of LLM reach.
"""

from __future__ import annotations

import os
import sqlite3
from contextlib import contextmanager
from typing import Any

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "insights.db")

_SCHEMA = [
    """CREATE TABLE IF NOT EXISTS market_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT,
        source TEXT,
        raw_json TEXT,
        fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""",
    """CREATE TABLE IF NOT EXISTS search_cache (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query TEXT UNIQUE,
        result TEXT,
        fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""",
    """CREATE TABLE IF NOT EXISTS analysis_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT,
        analysis TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""",
]


def init_db() -> None:
    os.makedirs(os.path.dirname(os.path.abspath(DB_PATH)), exist_ok=True)
    with _connect() as conn:
        for statement in _SCHEMA:
            conn.execute(statement)
        conn.commit()


@contextmanager
def _connect() -> Any:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def read_all() -> list[dict[str, Any]]:
    with _connect() as conn:
        rows = conn.execute("SELECT * FROM market_data ORDER BY fetched_at DESC").fetchall()
        return [dict(row) for row in rows]


def read_by_symbol(symbol: str) -> list[dict[str, Any]]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT * FROM market_data WHERE symbol = ? ORDER BY fetched_at DESC",
            (symbol.upper(),),
        ).fetchall()
        return [dict(row) for row in rows]


def read_search(query: str) -> dict[str, Any] | None:
    with _connect() as conn:
        row = conn.execute("SELECT * FROM search_cache WHERE query = ?", (query,)).fetchone()
        return dict(row) if row else None


def upsert_search(query: str, result: str) -> None:
    with _connect() as conn:
        conn.execute(
            """INSERT INTO search_cache (query, result)
               VALUES (?, ?)
               ON CONFLICT(query) DO UPDATE SET result = excluded.result, fetched_at = CURRENT_TIMESTAMP""",
            (query, result),
        )
        conn.commit()


def write_analysis(symbol: str, analysis: str) -> None:
    with _connect() as conn:
        conn.execute(
            "INSERT INTO analysis_log (symbol, analysis) VALUES (?, ?)",
            (symbol.upper(), analysis),
        )
        conn.commit()