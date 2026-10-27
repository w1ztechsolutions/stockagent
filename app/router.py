"""Model router with provider fallback for Phungu Insights.

Tries each provider in PROVIDER_ORDER until one returns a usable response.
"""

from __future__ import annotations

from typing import Any

from app.config import Settings
from app.providers.base import AssistantTurn, ChatMessage, ProviderError
from app.providers.openai_compat import OpenAICompatProvider


class _ProviderSettings:
    """Lightweight settings object for a single provider."""

    def __init__(self, name: str, base_url: str, api_key: str | None, model: str, enabled: bool = True, timeout: float = 60.0) -> None:
        self.name = name
        self.base_url = base_url
        self.api_key = api_key
        self.model = model
        self.enabled = enabled
        self.timeout = timeout


class ModelRouter:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.provider: OpenAICompatProvider | None = None
        self._providers: list[OpenAICompatProvider] = []
        self._build_providers()

    def _build_providers(self) -> None:
        for name in self.settings.PROVIDER_ORDER:
            name = name.strip().lower()
            if name == "ollama":
                prov = OpenAICompatProvider(
                    _ProviderSettings(
                        name="ollama",
                        base_url=getattr(self.settings, "OLLAMA_BASE_URL", "http://localhost:11434"),
                        api_key=None,
                        model=getattr(self.settings, "OLLAMA_MODEL", "llama3.1:8b"),
                        enabled=True,
                    )
                )
            elif name == "openrouter":
                prov = OpenAICompatProvider(
                    _ProviderSettings(
                        name="openrouter",
                        base_url="https://openrouter.ai/api/v1",
                        api_key=getattr(self.settings, "CLOUDFLARE_API_TOKEN", None),
                        model="anthropic/claude-3.5-sonnet",
                        enabled=bool(getattr(self.settings, "CLOUDFLARE_API_TOKEN", None)),
                    )
                )
            elif name == "gemini":
                prov = OpenAICompatProvider(
                    _ProviderSettings(
                        name="gemini",
                        base_url="https://generativelanguage.googleapis.com/v1beta",
                        api_key=getattr(self.settings, "GEMINI_API_KEY", None),
                        model="gemini-1.5-flash",
                        enabled=bool(getattr(self.settings, "GEMINI_API_KEY", None)),
                    )
                )
            elif name == "groq":
                prov = OpenAICompatProvider(
                    _ProviderSettings(
                        name="groq",
                        base_url="https://api.groq.com/openai/v1",
                        api_key=getattr(self.settings, "GROQ_API_KEY", None),
                        model="mixtral-8x7b-32768",
                        enabled=bool(getattr(self.settings, "GROQ_API_KEY", None)),
                    )
                )
            else:
                continue
            self._providers.append(prov)
        # Set the first available provider as the "active" one for model_used reporting
        for prov in self._providers:
            if prov.available():
                self.provider = prov
                break

    def chat(self, messages: list[ChatMessage], tools: list[dict[str, Any]] | None = None) -> AssistantTurn:
        last_error: ProviderError | None = None
        for prov in self._providers:
            if not prov.available():
                continue
            try:
                turn = prov.chat(messages, tools=tools)
                self.provider = prov
                return turn
            except ProviderError as exc:
                last_error = exc
                continue
        if last_error is not None:
            raise last_error
        raise ProviderError("router", "no providers available", retryable=False)