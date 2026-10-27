# Configuration

## Environment Variables

All configuration is managed via environment variables in `app/config.py`.

### Provider Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `PROVIDER_ORDER` | `ollama,openrouter,gemini,groq` | Comma-separated provider priority order |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama API base URL |
| `OLLAMA_MODEL` | `llama3.1:8b` | Default Ollama model |
| `GEMINI_API_KEY` | `""` | Google Gemini API key |
| `GROQ_API_KEY` | `""` | Groq API key |
| `CLOUDFLARE_API_TOKEN` | `""` | Cloudflare API token (used by OpenRouter config in router) |
| `CLOUDFLARE_ACCOUNT_ID` | `""` | Cloudflare account ID |

### Application Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `ADMIN_TOKEN` | `""` | Bearer token for admin endpoints (if empty, admin endpoints return 503) |
| `MAX_AGENT_STEPS` | `6` | Maximum reasoning/tool-calling iterations per request |
| `MAX_HISTORY` | `8` | Maximum conversation turns kept in history |
| `PORT` | `8080` | Server port (Render sets this automatically) |

## Settings Class

```python
class Settings:
    PROVIDER_ORDER: list = os.getenv("PROVIDER_ORDER", "ollama,openrouter,gemini,groq").split(",")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    CLOUDFLARE_API_TOKEN: str = os.getenv("CLOUDFLARE_API_TOKEN", "")
    CLOUDFLARE_ACCOUNT_ID: str = os.getenv("CLOUDFLARE_ACCOUNT_ID", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    ADMIN_TOKEN: str = os.getenv("ADMIN_TOKEN", "")
    MAX_AGENT_STEPS: int = int(os.getenv("MAX_AGENT_STEPS", "6"))
    MAX_HISTORY: int = int(os.getenv("MAX_HISTORY", "8"))
```

## Provider Configuration Details

### Ollama
- Base URL configurable via `OLLAMA_BASE_URL`
- Model via `OLLAMA_MODEL`
- No API key required
- Typically used as primary for local/self-hosted models

### OpenRouter
- Hardcoded base URL: `https://openrouter.ai/api/v1`
- Model: `anthropic/claude-3.5-sonnet` (hardcoded in router)
- Uses `CLOUDFLARE_API_TOKEN` as API key
- Enabled only if token is set

### Gemini
- Base URL: `https://generativelanguage.googleapis.com/v1beta`
- Model: `gemini-1.5-flash` (hardcoded)
- Uses `GEMINI_API_KEY`
- Enabled only if key is set

### Groq
- Base URL: `https://api.groq.com/openai/v1`
- Model: `mixtral-8x7b-32768` (hardcoded)
- Uses `GROQ_API_KEY`
- Enabled only if key is set

## Setup

1. Copy `.env.example` to `.env`
2. Configure provider credentials
3. Set `ADMIN_TOKEN` for admin endpoints
4. Adjust `MAX_AGENT_STEPS` and `MAX_HISTORY` as needed
5. Ensure `agent-render/data/insights.db` exists with market data
