"""OpenAI-compatible chat client used by Gemini, Groq, OpenRouter and Ollama."""

from __future__ import annotations

import json
import re
import time
from typing import Any

import httpx

from app.providers.base import AssistantTurn, ChatMessage, ProviderError, ToolCall

OLLAMA_PROBE_TTL = 15.0
OLLAMA_CONNECT_TIMEOUT = 0.4
ERROR_TEXT_LIMIT = 300

ZERO_WIDTH_CHARS = (0x200B, 0x200C, 0x200D, 0xFEFF)
ZERO_WIDTH = re.compile("[" + "".join(chr(code) for code in ZERO_WIDTH_CHARS) + "]")
TEXT_TOOL_CALL = re.compile(r"<tool_call\s*>(.*?)</tool_call\s*>", re.DOTALL | re.IGNORECASE)
TEXT_FUNCTION = re.compile(
    r"<function\s*=\s*([A-Za-z0-9_.\-]+)\s*>(.*?)</function\s*>", re.DOTALL | re.IGNORECASE
)
TEXT_PARAMETER = re.compile(
    r"<parameter\s*=\s*([A-Za-z0-9_.\-]+)\s*>(.*?)</parameter\s*>", re.DOTALL | re.IGNORECASE,
)


def _strip_tool_call_blocks(text: str) -> str:
    return ZERO_WIDTH.sub("", text)


def _parse_text_tool_calls(content: str) -> list[ToolCall]:
    """Recover tool calls that a model emitted as markup instead of as JSON."""
    text = _strip_tool_call_blocks(content)
    calls: list[ToolCall] = []
    for block in TEXT_TOOL_CALL.findall(text):
        for name, body in TEXT_FUNCTION.findall(block):
            arguments: dict[str, Any] = {}
            for key, value in TEXT_PARAMETER.findall(body):
                arguments[key] = value.strip()
            if not arguments:
                stripped = body.strip()
                if stripped.startswith("{"):
                    try:
                        parsed = json.loads(stripped)
                    except ValueError:
                        parsed = None
                    if isinstance(parsed, dict):
                        arguments = parsed
            calls.append(
                ToolCall(
                    id=f"text_call_{len(calls)}",
                    name=name,
                    arguments=arguments,
                )
            )
    return calls


class OpenAICompatProvider:
    def __init__(self, settings: Any) -> None:
        self.settings = settings
        self.name = settings.name
        base_url = settings.base_url.rstrip("/")
        self._endpoint = base_url + "/chat/completions"
        timeout = httpx.Timeout(getattr(settings, "timeout", 60.0), connect=10.0)
        self._client = httpx.Client(timeout=timeout)
        self._probe: tuple[float, bool] | None = None
    
    @property
    def _headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        api_key = getattr(self.settings, "api_key", None)
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        if self.name == "openrouter":
            headers["HTTP-Referer"] = "https://mse-portal.wiztechsol-info.workers.dev"
            headers["X-Title"] = "Phungu Insights"
        return headers

    def available(self) -> bool:
        if not getattr(self.settings, "enabled", True):
            return False
        if self.name == "ollama":
            return self._probe_ollama()
        return bool(getattr(self.settings, "api_key", None))

    def _probe_ollama(self) -> bool:
        now = time.monotonic()
        if self._probe is not None:
            checked_at, reachable = self._probe
            if now - checked_at < OLLAMA_PROBE_TTL:
                return reachable
        try:
            probe = httpx.Client(timeout=OLLAMA_CONNECT_TIMEOUT)
            try:
                resp = probe.get(f"{self.settings.base_url.rstrip('/')}/api/tags")
                reachable = resp.status_code == 200
            finally:
                probe.close()
        except Exception:
            reachable = False
        self._probe = (now, reachable)
        return reachable

    def chat(self, messages: list[ChatMessage], tools: list[dict[str, Any]] | None = None) -> AssistantTurn:
        payload: dict[str, Any] = {
            "model": getattr(self.settings, "model", "unknown"),
            "messages": [m.to_openai() for m in messages],
        }
        if tools:
            payload["tools"] = tools

        last_error: Exception | None = None
        for attempt in range(2):
            try:
                response = self._client.post(self._endpoint, json=payload, headers=self._headers)
                if response.status_code in (404, 429) or response.status_code >= 500:
                    err = ProviderError(
                        self.name,
                        f"HTTP {response.status_code}: {response.text[:ERROR_TEXT_LIMIT]}",
                        status=response.status_code,
                        retryable=True,
                    )
                    last_error = err
                    continue
                if response.status_code != 200:
                    err = ProviderError(
                        self.name,
                        f"HTTP {response.status_code}: {response.text[:ERROR_TEXT_LIMIT]}",
                        status=response.status_code,
                        retryable=False,
                    )
                    last_error = err
                    continue
                data = response.json()
                return self._parse(data)
            except ValueError as exc:
                raise ProviderError(self.name, "provider returned invalid JSON", retryable=True) from exc
            except httpx.HTTPError as exc:
                last_error = exc
        if last_error is not None:
            raise last_error
        raise ProviderError(self.name, "no models are configured")

    def _parse(self, data: Any) -> AssistantTurn:
        choices = data.get("choices") if isinstance(data, dict) else None
        if not choices or not isinstance(choices[0], dict):
            raise ProviderError(self.name, "provider returned no usable choices", retryable=True)
        message = choices[0].get("message") or {}
        if not isinstance(message, dict):
            message = {}
        content = message.get("content")
        if isinstance(content, list):
            content = "".join(part.get("text", "") for part in content if isinstance(part, dict))
        elif content is not None and not isinstance(content, str):
            content = str(content)
        calls: list[ToolCall] = []
        for index, raw in enumerate(message.get("tool_calls") or []):
            if not isinstance(raw, dict):
                continue
            function = raw.get("function") or {}
            name = function.get("name")
            if not name:
                continue
            arguments = function.get("arguments")
            if isinstance(arguments, str):
                try:
                    parsed = json.loads(arguments) if arguments.strip() else {}
                except ValueError:
                    parsed = {}
            elif isinstance(arguments, dict):
                parsed = arguments
            else:
                parsed = {}
            calls.append(
                ToolCall(
                    id=raw.get("id") or f"call_{self.name}_{index}",
                    name=name,
                    arguments=parsed,
                )
            )
        if not calls and content:
            recovered = _parse_text_tool_calls(content)
            if recovered:
                calls = recovered
                content = TEXT_TOOL_CALL.sub("", content).strip()
        return AssistantTurn(content=content, tool_calls=tuple(calls))

    def close(self) -> None:
        self._client.close()


def _is_retryable_status(status: int) -> bool:
    if status == 429 or status >= 500:
        return True
    return status not in (401, 403, 404)


def _short(text: str, limit: int = ERROR_TEXT_LIMIT) -> str:
    collapsed = " ".join((text or "").split())
    if len(collapsed) <= limit:
        return collapsed
    return collapsed[:limit] + "..."