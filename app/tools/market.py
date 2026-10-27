"""Market data tools for Phungu Insights.

These are read-only helpers. They never mutate the database.
"""

from __future__ import annotations

from typing import Any

from app.db import read_all, read_by_symbol

CURRENCY = "MWK"


def series_summary(points: list, field: str) -> dict:
    if not points:
        return {"mean": None, "min": None, "max": None}
    values = [p.get(field, 0) for p in points if p.get(field) is not None]
    if not values:
        return {"mean": None, "min": None, "max": None}
    return {"mean": sum(values) / len(values), "min": min(values), "max": max(values)}


def get_quote(symbol: str) -> dict[str, Any]:
    """Return the latest quote for *symbol* from the local database."""
    symbol = symbol.strip().upper()
    rows = read_by_symbol(symbol)
    if not rows:
        return {"found": False, "symbol": symbol, "error": "no price recorded for symbol"}
    row = rows[0]
    raw = row.get("raw_json", {})
    if not isinstance(raw, dict):
        raw = {}
    return {
        "found": True,
        "symbol": symbol,
        "currency": CURRENCY,
        "trade_date": str(row.get("fetched_at", "")) if row.get("fetched_at") else None,
        "close": raw.get("close_price"),
        "previous_close": raw.get("previous_close"),
        "change_percent": raw.get("change_percent"),
        "open": raw.get("open_price"),
        "volume": raw.get("volume"),
        "turnover": raw.get("turnover"),
        "pe_ratio": raw.get("pe_ratio"),
        "dividend_yield_percent": raw.get("dividend_yield_percent"),
        "pbv": raw.get("pbv"),
    }


def get_history(symbol: str, days: int = 120) -> dict[str, Any]:
    """Return price history for *symbol* from the local database."""
    symbol = symbol.strip().upper()
    days = max(5, min(730, int(days)))
    rows = read_by_symbol(symbol)
    points = []
    for row in rows:
        raw = row.get("raw_json", {})
        if isinstance(raw, dict):
            points.append({"trade_date": row.get("fetched_at"), "close_price": raw.get("close_price")})
    points.sort(key=lambda p: p["trade_date"] or "")
    return {
        "symbol": symbol,
        "currency": CURRENCY,
        "days": days,
        "as_of": points[-1]["trade_date"] if points else None,
        "summary": series_summary(points, "close_price"),
        "points": points[-60:],
    }


def screen(
    max_pe: float | None = None,
    min_dividend_yield: float | None = None,
    min_change_percent: float | None = None,
    max_change_percent: float | None = None,
    limit: int = 10,
) -> dict[str, Any]:
    """Screen stocks from the local database."""
    limit = max(1, min(17, int(limit)))
    rows = read_all()
    results = []
    for row in rows:
        raw = row.get("raw_json", {})
        if not isinstance(raw, dict):
            continue
        symbol = row.get("symbol", "")
        pe = raw.get("pe_ratio")
        div = raw.get("dividend_yield_percent")
        change = raw.get("change_percent")
        if max_pe is not None and pe is not None and pe > max_pe:
            continue
        if min_dividend_yield is not None and div is not None and div < min_dividend_yield:
            continue
        if min_change_percent is not None and change is not None and change < min_change_percent:
            continue
        if max_change_percent is not None and change is not None and change > max_change_percent:
            continue
        results.append({"symbol": symbol, **raw})
        if len(results) >= limit:
            break
    return {"results": results, "count": len(results), "currency": CURRENCY}