# Configuration

## Environment Variables

All configuration is managed via environment variables in `app/config.py`.

### Provider Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `PROVIDER_ORDER` | `openrouter,gemini,groq` | Comma-separated provider priority order |
| `OPENROUTER_API_KEY` | `""` | OpenRouter API key (get one at https://openrouter.ai/keys) |
| `OPENROUTER_MODELS` | 10 free models (see below) | Comma-separated OpenRouter models, tried in round-robin order within the provider |
| `GEMINI_API_KEY` | `""` | Google Gemini API key |
| `GEMINI_MODELS` | `gemini-1.5-flash` | Comma-separated Gemini models, round-robin within the provider |
| `GROQ_API_KEY` | `""` | Groq API key |
| `GROQ_MODELS` | `mixtral-8x7b-32768` | Comma-separated Groq models, round-robin within the provider |

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
    PROVIDER_ORDER: list = os.getenv("PROVIDER_ORDER", "openrouter,gemini,groq").split(",")
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_MODELS: list = _split(os.getenv("OPENROUTER_MODELS", _DEFAULT_OPENROUTER_MODELS))
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODELS: list = _split(os.getenv("GEMINI_MODELS", "gemini-1.5-flash"))
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODELS: list = _split(os.getenv("GROQ_MODELS", "mixtral-8x7b-32768"))
    ADMIN_TOKEN: str = os.getenv("ADMIN_TOKEN", "")
    MAX_AGENT_STEPS: int = int(os.getenv("MAX_AGENT_STEPS", "6"))
    MAX_HISTORY: int = int(os.getenv("MAX_HISTORY", "8"))
```

## Default OpenRouter Free Models

The default `OPENROUTER_MODELS` selects 10 free models chosen for code, debugging, reasoning, vision, and tool-calling:

| Model | Strength |
|-------|----------|
| `thinkingmachines/inkling-small:free` | Best free coding/multimodal agent (SWE-bench 80.2%) |
| `thinkingmachines/inkling:free` | Strong agentic + vision (1M context) |
| `nvidia/nemotron-3-ultra-550b-a55b:free` | Frontier reasoning + tool calling (55B active) |
| `google/gemma-4-31b-it:free` | Best vision + reasoning + code combo |
| `nvidia/nemotron-3.5-super-vl:free` | Multimodal vision with document/GUI understanding |
| `recursive/flint-v1.0:free` | Purpose-built coding agent (bug fixes, tests) |
| `google/gemma-4-26b-a4b-it:free` | Near-31B quality at ~1/8 compute |
| `nvidia/nemotron-3-super-120b-a12b:free` | Best structured output + long-context retention |
| `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` | Only free model with audio+video+image |
| `cohere/north-mini-code:free` | Lightweight coding fallback |

## Routing Behavior

- The router tries providers in `PROVIDER_ORDER` order.
- Within a provider, models are tried in round-robin order. A failing model is skipped and the next model is attempted before the provider is abandoned.
- The active provider/model is reported in `/health` and `/chat` responses.

## Updating Models Without Code Changes

To swap models on a deployed instance, update the `OPENROUTER_MODELS` (or `GEMINI_MODELS` / `GROQ_MODELS`) environment variable on the host — no code change or redeploy needed:

```bash
# Render dashboard or .env
OPENROUTER_MODELS=thinkingmachines/inkling-small:free,google/gemma-4-31b-it:free
```

## Setup

1. Copy `.env.example` to `.env`
2. Configure provider credentials
3. Set `ADMIN_TOKEN` for admin endpoints
4. Adjust `MAX_AGENT_STEPS` and `MAX_HISTORY` as needed
5. Ensure `agent-render/data/insights.db` exists with market data