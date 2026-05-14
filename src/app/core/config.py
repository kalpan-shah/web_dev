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
    APP_NAME: str = "My Todo App"

    API_V1_STR: str = "/api/v1"
    DEV_DB: str = "test.db"

    # region DB Info
    DB_USER: str = getenv("DB_USER")
    DB_PASSWORD: str = getenv("DB_PASSWORD")
    DB_NAME: str = getenv("DB_NAME")
    DB_PORT: int = int(getenv("DB_PORT"))
    DB_HOST: str = getenv("DB_HOST")
    # endregion

    Environment: ENV = ENV.DEV

    @property
    def db_url(self):
        print("here we go")
        match self.Environment:
            case ENV.DEV:
                url = "postgresql+asyncpg://" \
                "{}:{}@{}:{}/{}".format(self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_PORT, self.DB_NAME)
                print(url)
                return url
            case ENV.TEST:
                return "sqlite+aiosqlite:///{}".format(self.DEV_DB)

            # case ENV.PROD:
            #     return "postgresql+asyncpg://"

    @property
    def is_dev(self):
        return self.Environment == ENV.DEV


base_settings = Settings()
