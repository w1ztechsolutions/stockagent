import os

from dotenv import load_dotenv

load_dotenv()


def _split(value: str) -> list:
    """Split a comma-separated env value into a trimmed, non-empty list."""
    return [item.strip() for item in value.split(",") if item.strip()]


# Default OpenRouter free models (researched for code, debug, reasoning, vision,
# and tool-calling). Override via OPENROUTER_MODELS to swap models without
# touching the codebase.
_DEFAULT_OPENROUTER_MODELS = (
    "thinkingmachines/inkling-small:free,"
    "thinkingmachines/inkling:free,"
    "nvidia/nemotron-3-ultra-550b-a55b:free,"
    "google/gemma-4-31b-it:free,"
    "nvidia/nemotron-3.5-super-vl:free,"
    "recursive/flint-v1.0:free,"
    "google/gemma-4-26b-a4b-it:free,"
    "nvidia/nemotron-3-super-120b-a12b:free,"
    "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free,"
    "cohere/north-mini-code:free"
)


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

    @classmethod
    def validate(cls) -> bool:
        errors = []
        if not cls.OPENROUTER_API_KEY and not cls.GEMINI_API_KEY and not cls.GROQ_API_KEY:
            errors.append("At least one provider API key is required (OPENROUTER_API_KEY, GEMINI_API_KEY, or GROQ_API_KEY)")
        if errors:
            raise ValueError(f"Missing required settings: {', '.join(errors)}")
        return True