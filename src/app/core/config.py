"""
@file:          core/config.py
@description:   Centralized Configuration
@date:          21 April 2026
@last modified:   14 May 2026
@author:        Kalpan Shah
@version:       1.0.0
"""
from os import getenv
from pydantic_settings import BaseSettings
from enum import Enum
from dotenv import load_dotenv

load_dotenv()

class ENV(Enum):
    DEV = 0  # reload enabled
    TEST = 1
    PROD = 2


class Settings(BaseSettings):

    Environment: ENV = ENV[getenv("ENV", "DEV")]

    APP_NAME: str = "My Todo App"

    API_V1_STR: str = "/api/v1"
    DEV_DB: str = "test.db"

    match Environment:
        case ENV.DEV:
            DB_USER: str = getenv("LOCAL_DB_USER")
            DB_PASSWORD: str = getenv("LOCAL_DB_PASSWORD")
            DB_NAME: str = getenv("LOCAL_DB_NAME")
            DB_PORT: int = int(getenv("LOCAL_DB_PORT", "0"))
            DB_HOST: str = getenv("LOCAL_DB_HOST")

        case ENV.PROD:
            DB_USER: str = getenv("DB_USER")
            DB_PASSWORD: str = getenv("DB_PASSWORD")
            DB_NAME: str = getenv("DB_NAME")
            DB_PORT: int = int(getenv("DB_PORT", "0"))
            DB_HOST: str = getenv("DB_HOST")

        case ENV.TEST:
            DB_USER: str = getenv("TEST_DB_USER")
            DB_PASSWORD: str = getenv("TEST_DB_PASSWORD")
            DB_NAME: str = getenv("TEST_DB_NAME")
            DB_PORT: int = int(getenv("TEST_DB_PORT", "0"))
            DB_HOST: str = getenv("TEST_DB_HOST")

    @property
    def db_url(self):
        if self.DB_PORT:
            url = "postgresql+asyncpg://" \
            "{}:{}@{}:{}/{}".format(
                self.DB_USER, self.DB_PASSWORD, self.DB_HOST,
                self.DB_PORT, self.DB_NAME
            )
        else:
            url = "postgresql+asyncpg://" \
            "{}:{}@{}/{}".format(
                self.DB_USER, self.DB_PASSWORD,
                self.DB_HOST, self.DB_NAME
            )
        print(url)
        return url

    @property
    def is_dev(self):
        return self.Environment == ENV.DEV


base_settings = Settings()
