from contextlib import asynccontextmanager
from prometheus_client import Counter, Histogram
from time import time

REQUEST_COUNT = Counter(
    "request_count", "Total number of requests", ["method", "endpoint", "http_status"]
)

REQUEST_LATENCY = Histogram(
    "request_latency_seconds", "Request latency in seconds", ["method", "endpoint"]
)

# Auth & User metrics
USER_REGISTRATIONS = Counter(
    "users_registered_total",
    "Total number of registered users"
)

USER_LOGINS = Counter(
    "user_logins_total",
    "Total login attempts",
    labelnames=["status"]
)

# Todo metrics
TODOS_CREATED = Counter(
    "todos_created_total",
    "Total number of todos created"
)

TODOS_COMPLETED = Counter(
    "todos_completed_total",
    "Total number of todos marked completed"
)


# Helper function to record metrics
class RequestTimer:
    def __init__(self, method: str, endpoint: str):
        self.method = method
        self.endpoint = endpoint

    def __enter__(self):
        # self.start_time = REQUEST_LATENCY.labels(self.method, self.endpoint).time()
        self.start_time = time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # self.start_time.stop()
        elapsed_time = time() - self.start_time
        REQUEST_LATENCY.labels(self.method, self.endpoint).observe(elapsed_time)
