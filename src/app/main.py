# Imports
from fastapi import FastAPI
from contextlib import asynccontextmanager
from prometheus_client import Counter, Histogram
from prometheus_fastapi_instrumentator import Instrumentator
from app.core.logger import setup_logging

# Initialize the logging config
setup_logging()

from app.api.v1.router import api_router
from app.core.config import base_settings
from app.db.session import engine
from fastapi.middleware.cors import CORSMiddleware


from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor


# Initialize OpenTelemetry
trace.set_tracer_provider(TracerProvider(
    resource=Resource.create({
        "service.name": base_settings.APP_NAME
    })
))
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter())
)

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

    # Prometheus metrics
    Instrumentator().instrument(_app).expose(_app, endpoint="/metrics")

    # OpenTelemetry instrumentation
    FastAPIInstrumentor.instrument_app(_app)


    _app.include_router(api_router, prefix=base_settings.API_V1_STR)

    return _app


# Script
app = create_app()
