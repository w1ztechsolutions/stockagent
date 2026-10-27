# agent-render Deployment Plan

## Overview
Python FastAPI agent adapted from `agent-app/` for Render deployment with Cloudflare AI fallback.

## Architecture
- **Render Web Service**: FastAPI + uvicorn exposes `/chat`, `/health`, `/api/quote/{symbol}`
- **Cloudflare Worker**: Proxies `/api/agent/chat` to Render; serves chat UI
- **Session Memory**: Stateless (client-sent history capped at MAX_HISTORY)
- **LLM Strategy**: Primary: remote Ollama → Fallback: Cloudflare AI

## Key Files
- `requirements.txt` - Python dependencies
- `render.yaml` - Render deployment blueprint
- `app/main.py` - FastAPI application
- `app/config.py` - Environment configuration
- `app/router.py` - Model provider failover

## Deployment Steps
1. Create Render Web Service from `agent-render/` directory
2. Add environment variables in Render dashboard (OLLAMA_BASE_URL, NEON_DATABASE_URL, etc.)
3. Set Cloudflare KV namespace `AGENT_SESSIONS`
4. Update Cloudflare Worker with agent routes and proxy to Render
5. Deploy: `wrangler deploy` + Render auto-deploys

## Environment Variables
- `OLLAMA_BASE_URL` - Remote Ollama HTTPS URL (set as Render secret)
- `OLLAMA_MODEL` - Default model (e.g., llama3.1:8b)
- `NEON_DATABASE_URL` - Read-only Neon connection string
- `PROVIDER_ORDER` - ollama,openrouter,gemini,groq
- `MAX_AGENT_STEPS` - Max reasoning steps (default 6)
- `MAX_HISTORY` - Max conversation history turns (default 8)
- `CLOUDFLARE_API_TOKEN` - For Cloudflare AI fallback
- `CLOUDFLARE_ACCOUNT_ID` - Cloudflare account ID

## Risks
- Render free tier may spin down after inactivity
- Two services to operate (Render + Cloudflare)
- Remote Ollama must be publicly reachable