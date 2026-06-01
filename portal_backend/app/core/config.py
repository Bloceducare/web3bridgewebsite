from functools import lru_cache
from pathlib import Path

from pydantic import AliasChoices, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = "Web3Bridge Student Portal API"
    APP_ENV: str = Field(
        default="development",
        validation_alias=AliasChoices("APP_ENV", "ENVIROMENT"),
    )
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = True

    POSTGRES_HOST: str = Field(
        default="localhost",
        validation_alias=AliasChoices("POSTGRES_HOST", "DB_HOST"),
    )
    POSTGRES_PORT: int = Field(
        default=5432,
        validation_alias=AliasChoices("POSTGRES_PORT", "DB_PORT"),
    )
    POSTGRES_DB: str = Field(
        default="portal_v1",
        validation_alias=AliasChoices("POSTGRES_DB", "DB_NAME"),
    )
    POSTGRES_USER: str = Field(
        default="portal_user",
        validation_alias=AliasChoices("POSTGRES_USER", "DB_USER"),
    )
    POSTGRES_PASSWORD: str = Field(
        default="portal_password",
        validation_alias=AliasChoices("POSTGRES_PASSWORD", "DB_PASSWORD"),
    )
    POSTGRES_SCHEMA: str = "portal"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str | None = None
    SYNC_QUEUE_KEY: str = "portal:sync:jobs"
    SYNC_QUEUE_BLOCK_TIMEOUT_SECONDS: int = 5
    SYNC_WORKER_ERROR_RETRY_BASE_SECONDS: float = 1.0
    SYNC_WORKER_ERROR_RETRY_MAX_SECONDS: float = 30.0
    ONBOARD_CRON_INTERVAL_MINUTES: int = 20
    ONBOARD_CRON_ENABLED: bool = True
    ONBOARD_CURSOR_LAG_WARNING_SECONDS: float = 3600.0

    JWT_SECRET_KEY: str = Field(
        default="change-me",
        validation_alias=AliasChoices("JWT_SECRET_KEY", "SECRET_KEY"),
    )
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 6440 
    REFRESH_TOKEN_EXPIRE_DAYS: int = 90
    ACTIVATION_TOKEN_EXPIRE_HOURS: int = 168  # 7 days
    PASSWORD_RESET_TOKEN_EXPIRE_HOURS: int = 1
    INTERNAL_API_KEY: str = Field(
        default="change-me-internal-key",
        validation_alias=AliasChoices("INTERNAL_API_KEY", "PAYMENT_API_KEY"),
    )
    AUTOMATION_API_KEY: str = Field(
        default="",
        validation_alias=AliasChoices("AUTOMATION_API_KEY"),
    )
    PORTAL_FRONTEND_URL: str = "https://portal.web3bridge.com"

    DISCORD_BOT_API_URL: str = Field(
        default="https://dreadful-addia-web3bridge-84cd21c2.koyeb.app",
    )
    DISCORD_BOT_API_KEY: str = Field(default="")
    DISCORD_STUDENT_ROLE: str = Field(
        default="cohort-xv",
        validation_alias=AliasChoices("DISCORD_STUDENT_ROLE", "DISCORD_COHORT_ROLE"),
    )
    DISCORD_INVITE_CATEGORY_ID: str = Field(default="")

    EMAIL_HOST: str = Field(default="smtp.gmail.com")
    EMAIL_PORT: int = Field(default=587)
    EMAIL_HOST_USER: str = Field(default="")
    EMAIL_HOST_PASSWORD: str = Field(default="")
    EMAIL_USE_TLS: bool = True
    DEFAULT_FROM_EMAIL: str = Field(
        default="support@web3bridge.com",
        validation_alias=AliasChoices("DEFAULT_FROM_EMAIL", "EMAIL_HOST_USER"),
    )
    ADMISSION_EMAIL_HOST_USER: str = Field(default="")

    @model_validator(mode="after")
    def validate_production_security(self) -> "Settings":
        if self.APP_ENV.lower() not in {"production", "staging"}:
            return self

        errors: list[str] = []
        if self.DEBUG:
            errors.append("DEBUG must be false in production/staging")
        if self.JWT_SECRET_KEY == "change-me":
            errors.append("JWT_SECRET_KEY must be overridden in production/staging")
        if self.INTERNAL_API_KEY == "change-me-internal-key":
            errors.append("INTERNAL_API_KEY must be overridden in production/staging")
        if self.POSTGRES_PASSWORD == "portal_password":
            errors.append("POSTGRES_PASSWORD must be overridden in production/staging")
        if not self.PORTAL_FRONTEND_URL.startswith("https://"):
            errors.append("PORTAL_FRONTEND_URL must use https in production/staging")

        if errors:
            raise ValueError("; ".join(errors))
        return self

    @property
    def effective_automation_api_key(self) -> str:
        """API key for automation clients (API-Key header); falls back to INTERNAL_API_KEY."""
        return self.AUTOMATION_API_KEY or self.INTERNAL_API_KEY

    @property
    def postgres_dsn(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def redis_dsn(self) -> str:
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


@lru_cache
def get_settings() -> Settings:
    return Settings()
