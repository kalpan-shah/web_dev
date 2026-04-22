# Imports
from fastapi import FastAPI
from app.api.v1.router import api_router
from app.core.logger import setup_logging
from app.core.config import config

# Initialize the logging config
setup_logging()


# create app with factory
def create_app() -> FastAPI:
    _app = FastAPI(title=config.APP_NAME)

    _app.include_router(api_router, prefix=config.API_V1_STR)

    return _app


# Script
app = create_app()
