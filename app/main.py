from __future__ import annotations

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Header, status
from fastapi.responses import JSONResponse
from .config import Settings
from .agent import FinanceAgent
from .models import ChatRequest, ChatResponse, HealthResponse, QuoteResponse
from .db import init_db

settings = Settings()
agent = FinanceAgent(settings)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Phungu Agent", version="1.0.0", lifespan=lifespan)

ADMIN_TOKEN = settings.ADMIN_TOKEN if hasattr(settings, "ADMIN_TOKEN") else ""


def _require_admin(authorization: str | None = None) -> None:
    if not ADMIN_TOKEN:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Admin not configured")
    if authorization != f"Bearer {ADMIN_TOKEN}":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin token")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    database = "connected"
    provider_name = "unknown"
    model_name = "unknown"
    if agent.router.provider:
        provider_name = agent.router.provider.name
        model_name = getattr(agent.router.provider.settings, "model", "unknown")
    return HealthResponse(
        status="healthy",
        provider=provider_name,
        database=database,
        model=model_name,
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response = await agent.chat(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/quote/{symbol}", response_model=QuoteResponse)
async def get_quote(symbol: str):
    try:
        from .tools.market import get_quote as get_quote_tool

        result = get_quote_tool(symbol)
        if not result.get("found"):
            return QuoteResponse(
                symbol=symbol,
                found=False,
                error=result.get("error", "No quote found"),
            )
        return QuoteResponse(
            symbol=result.get("symbol", symbol),
            found=True,
            currency=result.get("currency", "MWK"),
            trade_date=result.get("trade_date"),
            close=result.get("close"),
            change_percent=result.get("change_percent"),
            pe_ratio=result.get("pe_ratio"),
            dividend_yield=result.get("dividend_yield_percent"),
        )
    except Exception as e:
        return QuoteResponse(
            symbol=symbol,
            found=False,
            error=str(e),
        )


@app.get("/api/providers")
async def list_providers(authorization: str | None = Header(default=None)):
    _require_admin(authorization)
    result = []
    for prov in agent.router._providers:
        result.append(
            {
                "name": prov.name,
                "enabled": prov.settings.enabled,
                "available": prov.available(),
                "model": getattr(prov.settings, "model", "unknown"),
                "base_url": prov.settings.base_url,
            }
        )
    return {"providers": result}


@app.post("/admin/session/{session_id}/clear")
async def clear_session(session_id: str, authorization: str | None = Header(default=None)):
    _require_admin(authorization)
    from .memory import MEMORY

    MEMORY.clear(session_id)
    return {"status": "cleared", "session_id": session_id}