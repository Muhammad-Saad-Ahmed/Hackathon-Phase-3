from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # Database settings
    database_url: str = "postgresql+asyncpg://username:password@localhost/dbname"

    @property
    def sync_database_url(self) -> str:
        """
        Convert async database URL to sync version for synchronous operations.
        Replaces asyncpg with psycopg (psycopg3 sync mode) and adds SSL for Neon.
        """
        url = self.database_url.replace("postgresql+asyncpg://", "postgresql+psycopg://")
        separator = "&" if "?" in url else "?"
        return f"{url}{separator}sslmode=require"

    # LLM settings
    llm_provider: str = "openai"
    llm_model: str = "gpt-4o"
    llm_base_url: Optional[str] = None
    llm_api_key: Optional[str] = None

    # OpenAI-specific settings
    openai_api_key: Optional[str] = None

    # MCP settings
    mcp_host: str = "localhost"
    mcp_port: int = 8001

    # Server settings
    server_host: str = "localhost"
    server_port: int = 8000
    request_timeout_seconds: float = 30.0

    # CORS settings (comma-separated list of allowed origins, "*" = allow all)
    cors_origins: str = "*"

    # Logging settings
    log_level: str = "INFO"

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "ignore"
    }


# Create a global settings instance
settings = Settings()