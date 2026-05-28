# Imports
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.v1.router import api_router
from app.core.logger import setup_logging
from app.core.config import base_settings
from app.db.session import engine
from fastapi.middleware.cors import CORSMiddleware

# Initialize the logging config
setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()

# create app with factory
def create_app() -> FastAPI:
    _app = FastAPI(title=base_settings.APP_NAME, lifespan=lifespan)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=base_settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.include_router(api_router, prefix=base_settings.API_V1_STR)

    return _app


# Script
app = create_app()
