# Architecture Overview

## System Design

The Phungu Agent follows a simple, modular architecture:

```
┌─────────────┐
│   Client     │
└─────┬───────┘
      │ HTTP
      ▼
┌─────────────────────────────────────────┐
│           FastAPI (main.py)              │
│  ┌─────────┐ ┌────────┐ ┌─────────────┐ │
│  │ /health │ │ /chat  │ │ /api/quote/* │ │
│  └─────────┘ └────────┘ └─────────────┘ │
└─────────────┬───────────────────────────┘
              │
              ▼
        ┌─────────────┐
        │ FinanceAgent │
        │   (agent.py) │
        └─────┬───────┘
              │
        ┌─────┴─────────────────────────────┐
        │                                   │
        ▼                                   ▼
    ┌────────┐                        ┌─────────┐
    │ Router │                        │ Memory  │
    │(router)│                        │(memory) │
    └───┬────┘                        └─────────┘
        │
        ▼
    ┌─────────────────────────────────────┐
    │         Providers (OpenAI Compat)    │
    │  Ollama → OpenRouter → Gemini → Groq│
    └─────────────────────────────────────┘
              │
              ▼
            Tools
        ┌───┴───┬─────────┬─────────┐
      market   market   screen   web
     get_quote get_hist           fetch_url
              │
              ▼
           SQLite DB
         (data/insights.db)
```

## Components

### FastAPI Application (`app/main.py`)
- Lifespan management initializes database
- Routes: health check, chat, quote endpoint, provider admin, session management
- Admin endpoints protected by `ADMIN_TOKEN` header

### FinanceAgent (`app/agent.py`)
- Orchestrates the agent loop with max steps (`MAX_AGENT_STEPS`)
- Builds system prompt with tool descriptions
- Manages conversation history from memory
- Executes tool calls and feeds results back to LLM
- Persists conversation turns to memory

### ModelRouter (`app/router.py`)
- Builds providers from `PROVIDER_ORDER` configuration
- Tries providers in order, falls back on `ProviderError`
- Sets active provider for reporting

### Providers (`app/providers/`)
- `base.py`: Abstract base classes and types
- `openai_compat.py`: OpenAI-compatible API client for all providers

### Tools (`app/tools/`)
- `market.py`: Read-only market data queries from SQLite
- `web.py`: URL fetching with SSRF protection and PDF/text extraction

### Memory (`app/memory.py`)
- In-memory session storage
- Capped history per session

### Database (`app/db.py`)
- Read-only access layer for SQLite
- Schema: `market_data`, `search_cache`, `analysis_log`

## Data Flow

1. Client sends `POST /chat` with message and optional session_id
2. Agent retrieves conversation history from memory
3. Router selects first available provider and calls it with messages + tool definitions
4. If LLM wants tools, agent executes them and loops back with results
5. When LLM provides final answer, agent saves to memory and returns response
6. Process repeats until final answer or `MAX_AGENT_STEPS` reached

## Design Principles

- **Read-only by default** - Tools don't mutate database; writes happen externally
- **Defensive** - SSRF protection, error handling, step limits
- **Provider-agnostic** - OpenAI-compatible interface allows easy provider swapping
- **Stateless deployment** - Works in serverless/container environments (Render)
- **Local-first data** - Uses pre-populated SQLite database for reliability
