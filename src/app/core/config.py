"""
@file:          core/config.py
@description:   Centralized Configuration management with environment-aware validation
@date:          21 April 2026
@last modified:   20 May 2026
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

    # 2. Authentication Variables
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    DB_USER: str | None = None
    DB_PASSWORD: str | None = None
    DB_NAME: str | None = None
    DB_PORT: int = 0
    DB_HOST: str | None = None

    LOCAL_DB_USER: str | None = None
    LOCAL_DB_PASSWORD: str | None = None
    LOCAL_DB_NAME: str | None = None
    LOCAL_DB_PORT: int = 0
    LOCAL_DB_HOST: str | None = None

    TEST_DB_USER: str | None = None
    TEST_DB_PASSWORD: str | None = None
    TEST_DB_NAME: str | None = None
    TEST_DB_PORT: int = 0
    TEST_DB_HOST: str | None = None

    # Tell Pydantic how to handle the .env source file
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  # Keeps things stable if extra fields are in the file
    )

    @model_validator(mode="after")
    def compute_environment_db_fields(self):
        """
        Runs right after validation. Inspects the active environment enum
        and maps the correct sub-variables onto the standard core DB fields.
        """
        match self.Environment:
            case ENV.DEV:
                self.DB_USER = self.LOCAL_DB_USER or self.DB_USER
                self.DB_PASSWORD = self.LOCAL_DB_PASSWORD or self.DB_PASSWORD
                self.DB_NAME = self.LOCAL_DB_NAME or self.DB_NAME
                self.DB_PORT = self.LOCAL_DB_PORT or self.DB_PORT
                self.DB_HOST = self.LOCAL_DB_HOST or self.DB_HOST

            case ENV.TEST:
                self.DB_USER = self.TEST_DB_USER or self.DB_USER
                self.DB_PASSWORD = self.TEST_DB_PASSWORD or self.DB_PASSWORD
                self.DB_NAME = self.TEST_DB_NAME or self.DB_NAME
                self.DB_PORT = self.TEST_DB_PORT or self.DB_PORT
                self.DB_HOST = self.TEST_DB_HOST or self.DB_HOST

            case ENV.PROD:
                # Production strings are already bound directly to primary fields,
                # but we validate that they aren't missing.
                if not all([self.DB_USER, self.DB_HOST, self.DB_NAME]):
                    raise ValueError("Production environment requires full base DB credentials.")

        return self

    @property
    def db_url(self) -> str:
        """Assembles the compiled SQLAlchemy connection URL dynamically."""
        if self.DB_PORT:
            return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_NAME}"

    @property
    def is_dev(self) -> bool:
        return self.Environment == ENV.DEV


base_settings = Settings()
