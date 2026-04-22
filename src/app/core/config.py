"""
@file:          core/config.py
@description:   Centralized Configuration
@date:          21 April 2026
@author:        Kalpan Shah
@version:       1.0.0
"""

from pydantic_settings import BaseSettings
from enum import Enum


class ENV(Enum):
    DEV = 0  # reload enabled
    TEST = 1
    PROD = 2


class Settings(BaseSettings):
    APP_NAME: str = "My Todo App"

    API_V1_STR: str = "/api/v1"
    DEV_DB: str = "test.db"

    Environment: ENV = ENV.DEV

    @property
    def db_url(self):
        match self.Environment:
            case ENV.DEV:
                return "sqlite:///./{}".format(self.DEV_DB)


config = Settings()
