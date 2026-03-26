from fastapi import FastAPI
from app.api.v1.router import api_router


def create_app() -> FastAPI:
    app = FastAPI(title="Todo API")

    app.include_router(api_router, prefix="/api/v1")

    return app


# Script
app = create_app()