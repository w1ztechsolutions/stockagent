import os


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

    @classmethod
    def validate(cls) -> bool:
        errors = []
        if not cls.OLLAMA_BASE_URL:
            errors.append("OLLAMA_BASE_URL is required")
        if errors:
            raise ValueError(f"Missing required settings: {', '.join(errors)}")
        return True