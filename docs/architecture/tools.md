# Tools Reference

The agent has access to the following read-only tools defined in `app/agent.py`.

## Tool Definitions

### get_quote
Get the latest stock quote for a symbol from the Malawi Stock Exchange.

**Parameters:**
- `symbol` (string, required) - Stock symbol (e.g., TNM, FMB, NBM)

**Returns:** Dict with quote data from local database
- `found` (bool)
- `symbol` (string)
- `currency` (string, default "MWK")
- `trade_date` (string|null)
- `close` (float|null)
- `previous_close` (float|null)
- `change_percent` (float|null)
- `open` (float|null)
- `volume` (int|null)
- `turnover` (float|null)
- `pe_ratio` (float|null)
- `dividend_yield_percent` (float|null)
- `pbv` (float|null)

**Source:** `app/tools/market.py:get_quote()`

### get_history
Get historical price data for a stock symbol.

**Parameters:**
- `symbol` (string, required) - Stock symbol (e.g., TNM, FMB, NBM)
- `days` (integer, optional) - Number of days of history (default 120, clamped 5-730)

**Returns:**
- `symbol` (string)
- `currency` (string)
- `days` (int)
- `as_of` (string|null)
- `summary` (dict) - mean, min, max of close prices
- `points` (list) - Up to 60 most recent data points with `trade_date` and `close_price`

**Source:** `app/tools/market.py:get_history()`

### screen
Screen stocks by P/E, dividend yield, or change percent.

**Parameters:**
- `max_pe` (number, optional) - Maximum P/E ratio
- `min_dividend_yield` (number, optional) - Minimum dividend yield percent
- `min_change_percent` (number, optional) - Minimum change percent
- `max_change_percent` (number, optional) - Maximum change percent
- `limit` (integer, optional) - Maximum results (default 10, clamped 1-17)

**Returns:**
- `results` (list) - Matching stocks with raw data
- `count` (int)
- `currency` (string)

**Source:** `app/tools/market.py:screen()`

### fetch_url
Fetch a public URL and extract its text content (PDF or HTML).

**Parameters:**
- `url` (string, required) - URL to fetch (http/https only)

**Returns:**
- `found` (bool)
- `url` (string)
- `content_type` (string)
- `content` (string) - Extracted text (truncated to 8000 chars)
- `source` (string) - "mse_reports", "pdf", "webpage", or error source

**Security Features:**
- Only allows http/https schemes
- Resolves DNS and blocks private/link-local/reserved/loopback IPs (SSRF protection)
- Follows redirects (max 5)
- Timeout: 10 seconds
- Max content: 200KB bytes, text truncated to 8000 chars
- User-Agent: `Mozilla/5.0 (compatible; PhunguInsightsBot/1.0; +https://mse-portal.wiztechsol-info.workers.dev)`

**PDF Support:** Uses PyMuPDF (`fitz`) if available, otherwise returns byte count message.

**Source:** `app/tools/web.py:fetch_url()`

## Tool Usage Guidelines

- Tools are only called when the LLM decides to use them (function calling)
- All tools are read-only - they never write to the database
- Market tools read from local SQLite database only
- Tool results are JSON-serialized and fed back to the LLM
- Invalid arguments return error messages
- Tool failures are caught and returned as errors

## System Prompt

The agent uses this system prompt (from `app/agent.py`):

```
You are a Malawi Stock Exchange finance assistant.

Available tools:
- get_quote(symbol): Latest stock quote for an MSE symbol.
- get_history(symbol, days): Historical price data.
- screen(max_pe, min_dividend_yield, min_change_percent, max_change_percent, limit): Screen stocks.
- fetch_url(url): Fetch a public URL (PDF or HTML).

Always use tools when the user asks about specific stocks, prices, or market data. Do not fabricate data.
```
