"""
@file:          core/config.py
@description:   Centralized Configuration management with environment-aware validation
@date:          21 April 2026
@last modified:   28 May 2026
@author:        Kalpan Shah
@version:       1.0.0
"""
from enum import Enum
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class ENV(Enum):
    DEV = "DEV"
    TEST = "TEST"
    PROD = "PROD"


class Settings(BaseSettings):
    # 1. Base Settings
    Environment: ENV = ENV.DEV
    APP_NAME: str = "My Todo App"
    API_V1_STR: str = "/api/v1"

    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]

    # 2. Authentication Variables
    JWT_SECRET_KEY: str = "super_secret_key_it_must_be_atleast_32_characters_long_for_security"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15 # 15 minutes

    # 3. Database
    DB_URL: str | None = None

    DB_USER: str | None = None
    DB_PASSWORD: str | None = None
    DB_NAME: str | None = None
    DB_PORT: int | None = None
    DB_HOST: str | None = None

    LOCAL_DB_USER: str | None = None
    LOCAL_DB_PASSWORD: str | None = None
    LOCAL_DB_NAME: str | None = None
    LOCAL_DB_PORT: int | None = None
    LOCAL_DB_HOST: str | None = None

    TEST_DB_USER: str | None = None
    TEST_DB_PASSWORD: str | None = None
    TEST_DB_NAME: str | None = None
    TEST_DB_PORT: int | None = None
    TEST_DB_HOST: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        str_strip_whitespace=True,
    )

    @model_validator(mode="before")
    @classmethod
    def compute_environment_db_fields(cls, values: dict) -> dict:
        """
        Runs before model initialization.
        If DB_URL is not directly provided, constructs it based on the active Environment.
        """
        if not isinstance(values, dict):
            return values

        # Highest priority: Use direct DB_URL if provided
        if values.get("DB_URL"):
            return values

        env = values.get("Environment", "DEV")  # Default to DEV if not set

        # Handle both string and Enum (important in 'before' mode)
        if env in (ENV.DEV, "DEV", "dev"):
            values["DB_USER"] = values.get("LOCAL_DB_USER") or values.get("DB_USER")
            values["DB_PASSWORD"] = values.get("LOCAL_DB_PASSWORD") or values.get("DB_PASSWORD")
            values["DB_NAME"] = values.get("LOCAL_DB_NAME") or values.get("DB_NAME")
            values["DB_PORT"] = values.get("LOCAL_DB_PORT") or values.get("DB_PORT")
            values["DB_HOST"] = values.get("LOCAL_DB_HOST") or values.get("DB_HOST")

        elif env in (ENV.TEST, "TEST", "test"):
            values["DB_USER"] = values.get("TEST_DB_USER") or values.get("DB_USER")
            values["DB_PASSWORD"] = values.get("TEST_DB_PASSWORD") or values.get("DB_PASSWORD")
            values["DB_NAME"] = values.get("TEST_DB_NAME") or values.get("DB_NAME")
            values["DB_PORT"] = values.get("TEST_DB_PORT") or values.get("DB_PORT")
            values["DB_HOST"] = values.get("TEST_DB_HOST") or values.get("DB_HOST")

        elif env in (ENV.PROD, "PROD", "prod"):
            if not all([values.get(k) for k in ("DB_USER", "DB_HOST", "DB_NAME")]):
                raise ValueError("Production environment requires full base DB credentials.")

        # Build DB_URL
        user = values.get("DB_USER")
        password = values.get("DB_PASSWORD")
        host = values.get("DB_HOST")
        port = int(values.get("DB_PORT") or 0)
        name = values.get("DB_NAME")

        if not all([user, password, host, name]):
            raise ValueError(f"Missing database credentials for environment: {env}")

        values["DB_URL"] = cls.get_db_url(user, password, host, port, name)

        return values

    @staticmethod
    def get_db_url(user: str, password: str, host: str, port: int | None, name: str) -> str:
        """Construct PostgreSQL asyncpg URL."""
        if port and port > 0:
            return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"
        return f"postgresql+asyncpg://{user}:{password}@{host}/{name}"

    @property
    def db_url(self) -> str:
        """Recommended way to access database URL throughout the app."""
        if self.DB_URL is None:
            raise ValueError("DB_URL was not configured")
        return self.DB_URL

    @property
    def is_dev(self) -> bool:
        return self.Environment == ENV.DEV


base_settings = Settings()