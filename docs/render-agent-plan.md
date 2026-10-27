# agent-render Deployment Plan

## Overview
Python FastAPI agent adapted from `agent-app/` for Render deployment with multi-provider LLM fallback.

## Architecture
- **Render Web Service**: FastAPI + uvicorn exposes `/chat`, `/health`, `/api/quote/{symbol}`
- **Cloudflare Worker**: Proxies `/api/agent/chat` to Render; serves chat UI
- **Session Memory**: Stateless (client-sent history capped at MAX_HISTORY)
- **LLM Strategy**: Primary: OpenRouter → Fallback: Gemini → Groq

## Key Files
- `requirements.txt` - Python dependencies
- `render.yaml` - Render deployment blueprint
- `app/main.py` - FastAPI application
- `app/config.py` - Environment configuration
- `app/router.py` - Model provider failover

## Deployment Steps
1. Create Render Web Service from `agent-render/` directory
2. Add environment variables in Render dashboard (OPENROUTER_API_KEY, GEMINI_API_KEY, GROQ_API_KEY, etc.)
3. Set Cloudflare KV namespace `AGENT_SESSIONS`
4. Update Cloudflare Worker with agent routes and proxy to Render
5. Deploy: `wrangler deploy` + Render auto-deploys

## Environment Variables
- `NEON_DATABASE_URL` - Read-only Neon connection string (optional, uses local SQLite if unset)
- `PROVIDER_ORDER` - openrouter,gemini,groq
- `MAX_AGENT_STEPS` - Max reasoning steps (default 6)
- `MAX_HISTORY` - Max conversation history turns (default 8)
- `OPENROUTER_API_KEY` - OpenRouter API key (get one at https://openrouter.ai/keys)
- `OPENROUTER_MODELS` - Comma-separated OpenRouter models, round-robin within the provider (10 free models by default)
- `GEMINI_API_KEY` - Google Gemini API key
- `GEMINI_MODELS` - Comma-separated Gemini models, round-robin within the provider
- `GROQ_API_KEY` - Groq API key
- `GROQ_MODELS` - Comma-separated Groq models, round-robin within the provider

## Updating Models
To swap models on a deployed instance, update the `OPENROUTER_MODELS` (or `GEMINI_MODELS` / `GROQ_MODELS`) env var on the host — no code change or redeploy needed. See [Configuration](./architecture/configuration.md).

## Risks
- Render free tier may spin down after inactivity
- Two services to operate (Render + Cloudflare)