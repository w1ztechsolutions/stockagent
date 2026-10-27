# Phungu Agent (agent-render) Documentation

**Location:** `agent-render/`  
**Version:** 1.0.0  
**Framework:** FastAPI (Python)  
**Purpose:** Malawi Stock Exchange (MSE) finance assistant API

## Overview

The Phungu Agent is a FastAPI-based service that provides an AI-powered assistant for querying Malawi Stock Exchange market data. It orchestrates LLM calls across multiple providers with fallback logic, executes read-only tools against local market data, and maintains session memory.

## What This Agent Can Do

### Core Capabilities

- **Conversational AI Interface** - Accepts natural language queries via `/chat` endpoint with session-based conversation history
- **Multi-Provider LLM Routing** - Automatically tries providers in order (Ollama, OpenRouter, Gemini, Groq) with automatic fallback on failure
- **Market Data Tools** (Read-Only)
  - `get_quote(symbol)` - Get latest quote for an MSE symbol from local database
  - `get_history(symbol, days)` - Get historical price data (5-730 days range, returns up to 60 points)
  - `screen(...)` - Screen stocks by P/E, dividend yield, change percent
- **Web Content Retrieval** - `fetch_url(url)` to fetch and extract text from public HTML/PDF URLs with SSRF protection
- **Session Management** - In-memory conversation history per session (capped by `MAX_HISTORY`)
- **Health Monitoring** - `/health` endpoint reports provider, model, and database status
- **Admin Operations** - Clear sessions and inspect providers (protected by `ADMIN_TOKEN`)

### Data Access

- **Read-only SQLite database** at `agent-render/data/insights.db` with tables: `market_data`, `search_cache`, `analysis_log`
- All database mutations go through controlled helpers; the agent cannot directly write to the database
- Market data is sourced from MSE via the ETL pipeline in the main project

### Security Features

- **SSRF Protection** in `fetch_url`: blocks private/link-local/reserved IP addresses, only allows http/https schemes
- **Admin Authentication**: Bearer token required for `/api/providers` and session clearing
- **Read-only Tools**: Market tools only read from the database, no mutations
- **Request Limits**: `MAX_AGENT_STEPS` limits reasoning iterations (default 6)

## What This Agent Cannot Do (Not Implemented)

- **Direct Database Writes** - The agent has no tools to insert/update/delete market data. Mutations only happen via ETL processes outside the agent.
- **User Authentication/Authorization** - No user accounts, just session IDs; only admin endpoints use token auth
- **Trading/Order Placement** - No integration with brokers or trading systems
- **Real-time MSE API Calls** - Tools read from local SQLite database only, not live MSE APIs
- **Persistent Session Storage** - Memory is in-process only (`app/memory.py`), lost on restart
- **Rate Limiting** - No rate limiting implemented
- **Caching of LLM Responses** - No response caching
- **File Uploads** - No file upload endpoints
- **Streaming Responses** - Returns full responses, no SSE/streaming
- **Multi-turn Tool Chaining Beyond Steps Limit** - Capped at `MAX_AGENT_STEPS` (default 6)

## Planned Enhancements

See [render-agent-plan.md](./render-agent-plan.md) for deployment planning. Potential future work (not currently implemented):
- Persistent session storage (Redis/KV)
- Additional screening criteria
- Portfolio analysis tools
- Integration with live data sources
- Streaming responses

## Quick Start

### Local Development

```bash
cd agent-render
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env  # Configure your settings
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

### Environment Variables

See [.env.example](../.env.example) and [Configuration](./architecture/configuration.md) for details.

### API Documentation

When running, visit `http://localhost:8080/docs` for interactive Swagger documentation.

## Project Structure

```
agent-render/
├── app/
│   ├── __init__.py
│   ├── agent.py          # FinanceAgent orchestration
│   ├── config.py         # Settings
│   ├── db.py             # SQLite read layer
│   ├── main.py           # FastAPI app
│   ├── memory.py         # Session memory
│   ├── models.py         # Pydantic models
│   ├── router.py         # Provider routing/fallback
│   ├── providers/        # LLM providers
│   │   ├── base.py
│   │   └── openai_compat.py
│   └── tools/            # Agent tools
│       ├── __init__.py
│       ├── market.py
│       └── web.py
├── data/
│   └── insights.db       # Market data
├── docs/                 # Documentation
├── .env.example
├── models.txt
├── render.yaml           # Render deployment config
└── requirements.txt
```

## Related Documentation

- [Architecture Overview](./architecture/overview.md)
- [API Reference](./api/reference.md)
- [Configuration](./architecture/configuration.md)
- [Tools Reference](./architecture/tools.md)
- [Deployment Guide](./render-agent-plan.md)
- [Legal Documents](./legal/README.md)
