# API Reference

Base URL (local): `http://localhost:8080`  
Version: 1.0.0

## Endpoints

### GET /health
Health check endpoint.

**Response Model:** `HealthResponse`

```json
{
  "status": "healthy",
  "provider": "ollama",
  "database": "connected",
  "model": "llama3.1:8b"
}
```

**Fields:**
- `status` (string) - Service status
- `provider` (string) - Active LLM provider name
- `database` (string) - Database status
- `model` (string) - Active model name

---

### POST /chat
Chat with the finance agent.

**Request Model:** `ChatRequest`

```json
{
  "message": "What's the current price of TNM?",
  "session_id": "optional-session-id",
  "history": []
}
```

**Fields:**
- `message` (string, required) - User message
- `session_id` (string, optional) - Session identifier (auto-generated if not provided)
- `history` (array, optional) - Conversation history (not actively used, agent uses memory)

**Response Model:** `ChatResponse`

```json
{
  "response": "TNM (Telekom Networks Malawi) is currently trading at...",
  "session_id": "session_1234567890",
  "model_used": "ollama",
  "steps": 2
}
```

**Fields:**
- `response` (string) - Assistant response
- `session_id` (string) - Session ID
- `model_used` (string) - Model that generated response
- `steps` (int) - Agent steps taken (tool calls + reasoning iterations)

**Errors:** 500 on exceptions

---

### GET /api/quote/{symbol}
Get quote for a specific symbol (direct tool access).

**Parameters:**
- `symbol` (string, path) - Stock symbol

**Response Model:** `QuoteResponse`

```json
{
  "symbol": "TNM",
  "found": true,
  "currency": "MWK",
  "trade_date": "2026-10-27T05:00:00",
  "close": 450.5,
  "change_percent": 2.3,
  "pe_ratio": 12.5,
  "dividend_yield": 3.2
}
```

**Fields:**
- `symbol` (string)
- `found` (bool)
- `currency` (string, default "MWK")
- `trade_date` (string|null)
- `close` (float|null)
- `change_percent` (float|null)
- `pe_ratio` (float|null)
- `dividend_yield` (float|null)
- `error` (string|null)

Returns found=false with error if symbol not found.

---

### GET /api/providers
List configured providers (admin only).

**Headers:**
- `Authorization` (string, required) - `Bearer {ADMIN_TOKEN}`

**Response:**

```json
{
  "providers": [
    {
      "name": "ollama",
      "enabled": true,
      "available": true,
      "model": "llama3.1:8b",
      "base_url": "http://localhost:11434"
    },
    {
      "name": "openrouter",
      "enabled": false,
      "available": false,
      "model": "anthropic/claude-3.5-sonnet",
      "base_url": "https://openrouter.ai/api/v1"
    }
  ]
}
```

**Errors:**
- 503 if ADMIN_TOKEN not configured
- 401 if invalid token

---

### POST /admin/session/{session_id}/clear
Clear a session's memory (admin only).

**Headers:**
- `Authorization` (string, required) - `Bearer {ADMIN_TOKEN}`

**Response:**

```json
{
  "status": "cleared",
  "session_id": "session_1234567890"
}
```

**Errors:**
- 503 if ADMIN_TOKEN not configured
- 401 if invalid token

## Models

See `app/models.py` for Pydantic model definitions.

## Interactive Documentation

When the server is running, visit:
- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI JSON: `/openapi.json`
