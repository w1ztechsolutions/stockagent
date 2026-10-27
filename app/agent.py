"""Finance agent that orchestrates LLM calls, tools, and memory."""

from __future__ import annotations

import json
import re
import time
from typing import Any

from app.config import Settings
from app.db import read_by_symbol, read_all
from app.memory import MEMORY
from app.models import ChatRequest, ChatResponse
from app.providers.base import AssistantTurn, ChatMessage as ProviderMessage, ProviderError
from app.providers.openai_compat import OpenAICompatProvider
from app.router import ModelRouter
from app.tools.market import get_quote, get_history, screen
from app.tools.web import fetch_url

TOOL_MAP: dict[str, Any] = {
    "get_quote": get_quote,
    "get_history": get_history,
    "screen": screen,
    "fetch_url": fetch_url,
}

TOOL_DEFINITIONS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "get_quote",
            "description": "Get the latest stock quote for a symbol from the Malawi Stock Exchange.",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Stock symbol (e.g. TNM, FMB, NBM)"},
                },
                "required": ["symbol"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_history",
            "description": "Get historical price data for a stock symbol.",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Stock symbol (e.g. TNM, FMB, NBM)"},
                    "days": {"type": "integer", "description": "Number of days of history (default 120)"},
                },
                "required": ["symbol"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "screen",
            "description": "Screen stocks by P/E, dividend yield, or change percent.",
            "parameters": {
                "type": "object",
                "properties": {
                    "max_pe": {"type": "number", "description": "Maximum P/E ratio"},
                    "min_dividend_yield": {"type": "number", "description": "Minimum dividend yield percent"},
                    "min_change_percent": {"type": "number", "description": "Minimum change percent"},
                    "max_change_percent": {"type": "number", "description": "Maximum change percent"},
                    "limit": {"type": "integer", "description": "Maximum results to return (default 10)"},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_url",
            "description": "Fetch a public URL and extract its text content (PDF or HTML).",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "URL to fetch (http/https only)"},
                },
                "required": ["url"],
            },
        },
    },
]


class FinanceAgent:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or Settings()
        self.router = ModelRouter(self.settings)
        self.steps = 0

    def _build_system_prompt(self) -> str:
        return """You are a Malawi Stock Exchange finance assistant.

Available tools:
- get_quote(symbol): Latest stock quote for an MSE symbol.
- get_history(symbol, days): Historical price data.
- screen(max_pe, min_dividend_yield, min_change_percent, max_change_percent, limit): Screen stocks.
- fetch_url(url): Fetch a public URL (PDF or HTML).

Always use tools when the user asks about specific stocks, prices, or market data. Do not fabricate data.
"""

    async def chat(self, request: ChatRequest) -> ChatResponse:
        self.steps = 0
        session_id = request.session_id or f"session_{int(time.time())}"

        history = MEMORY.get_history(session_id)

        messages: list[ProviderMessage] = [
            ProviderMessage(role="system", content=self._build_system_prompt())
        ]
        for m in history[-self.settings.MAX_HISTORY :]:
            messages.append(
                ProviderMessage(
                    role=m.role,
                    content=m.content or "",
                    tool_calls=[],
                )
            )
        messages.append(ProviderMessage(role="user", content=request.message))

        last_turn: AssistantTurn | None = None
        while self.steps < self.settings.MAX_AGENT_STEPS:
            self.steps += 1
            try:
                turn = self.router.chat(messages, tools=TOOL_DEFINITIONS)
            except ProviderError as exc:
                return ChatResponse(
                    response=f"Provider error: {exc.message}",
                    session_id=session_id,
                    model_used=self.settings.PROVIDER_ORDER[0] if self.settings.PROVIDER_ORDER else "unknown",
                    steps=self.steps,
                )

            last_turn = turn

            if turn.wants_tools:
                messages.append(ProviderMessage(role="assistant", content=turn.content or "", tool_calls=list(turn.tool_calls)))

                tool_results: list[ProviderMessage] = []
                for call in turn.tool_calls:
                    func = TOOL_MAP.get(call.name)
                    if func is None:
                        result = {"error": f"Unknown tool: {call.name}"}
                    else:
                        try:
                            result = func(**call.arguments)
                        except TypeError as exc:
                            result = {"error": f"Invalid arguments for {call.name}: {exc}"}
                        except Exception as exc:  # noqa: BLE001
                            result = {"error": f"Tool {call.name} failed: {exc}"}
                    tool_results.append(
                        ProviderMessage(role="tool", content=json.dumps(result), tool_call_id=call.id)
                    )
                messages.extend(tool_results)
                continue

            assistant_content = turn.content or ""
            messages.append(ProviderMessage(role="assistant", content=assistant_content))

            MEMORY.add(session_id, ProviderMessage(role="user", content=request.message))
            MEMORY.add(session_id, ProviderMessage(role="assistant", content=assistant_content))

            return ChatResponse(
                response=assistant_content,
                session_id=session_id,
                model_used=getattr(self.router.provider, "name", "unknown")
                if self.router.provider
                else "unknown",
                steps=self.steps,
            )

        return ChatResponse(
            response="I've reached the maximum reasoning steps. Please try a simpler question.",
            session_id=session_id,
            model_used=getattr(self.router.provider, "name", "unknown")
            if self.router.provider
            else "unknown",
            steps=self.steps,
        )