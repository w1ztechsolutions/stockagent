"""Model router with provider fallback for Phungu Insights.

Tries each provider in PROVIDER_ORDER until one returns a usable response.
Within a provider, models are tried in round-robin order so a single failing
model doesn't block the provider and traffic spreads across the configured
models.
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


class _ProviderEntry:
    """A provider with one or more models and a round-robin cursor."""

    def __init__(self, name: str, base_url: str, api_key: str | None, models: list[str], enabled: bool) -> None:
        self.name = name
        self.base_url = base_url
        self.api_key = api_key
        self.models = list(models)
        self.enabled = enabled
        self._cursor = 0

    def available(self) -> bool:
        return self.enabled and bool(self.api_key) and bool(self.models)

    def next_model(self) -> str:
        if not self.models:
            return ""
        model = self.models[self._cursor % len(self.models)]
        self._cursor += 1
        return model

    def make_provider(self) -> OpenAICompatProvider:
        return OpenAICompatProvider(
            _ProviderSettings(
                name=self.name,
                base_url=self.base_url,
                api_key=self.api_key,
                model=self.next_model(),
                enabled=self.enabled,
            )
        )


class ModelRouter:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.provider: OpenAICompatProvider | None = None
        self._providers: list[_ProviderEntry] = []
        self._build_providers()

    def _build_providers(self) -> None:
        for name in self.settings.PROVIDER_ORDER:
            name = name.strip().lower()
            if name == "openrouter":
                entry = _ProviderEntry(
                    name="openrouter",
                    base_url="https://openrouter.ai/api/v1",
                    api_key=self.settings.OPENROUTER_API_KEY,
                    models=self.settings.OPENROUTER_MODELS,
                    enabled=bool(self.settings.OPENROUTER_API_KEY),
                )
            elif name == "gemini":
                entry = _ProviderEntry(
                    name="gemini",
                    base_url="https://generativelanguage.googleapis.com/v1beta",
                    api_key=self.settings.GEMINI_API_KEY,
                    models=self.settings.GEMINI_MODELS,
                    enabled=bool(self.settings.GEMINI_API_KEY),
                )
            elif name == "groq":
                entry = _ProviderEntry(
                    name="groq",
                    base_url="https://api.groq.com/openai/v1",
                    api_key=self.settings.GROQ_API_KEY,
                    models=self.settings.GROQ_MODELS,
                    enabled=bool(self.settings.GROQ_API_KEY),
                )
            else:
                continue
            self._providers.append(entry)
        # Set the first available provider as the "active" one for model_used reporting
        for entry in self._providers:
            if entry.available():
                self.provider = entry.make_provider()
                break

    def chat(self, messages: list[ChatMessage], tools: list[dict[str, Any]] | None = None) -> AssistantTurn:
        last_error: ProviderError | None = None
        for entry in self._providers:
            if not entry.available():
                continue
            # Try every configured model for this provider before giving up.
            for _ in range(len(entry.models)):
                prov = entry.make_provider()
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