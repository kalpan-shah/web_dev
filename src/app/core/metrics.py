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
TODO_CREATED = Counter(
    "todos_created_total",
    "Total number of todos created"
)

TODO_COMPLETED = Counter(
    "todos_completed_total",
    "Total number of todos marked completed"
)

TODO_UPDATED = Counter(
    "todos_updated_total",
    "Total number of todos updated"
)

TODO_FETCHED = Counter(
    "todos_fetched_total",
    "Total number of todos fetched"
)

TODO_DELETED = Counter(
    "todos_deleted_total",
    "Total number of todos deleted",
    labelnames=["status"]
)


# TODO: Remove the RequestTimer and its refrences from the codebase 
# and use a middleware to record metrics for all endpoints. 
# This will ensure that metrics are recorded consistently across all
# endpoints without needing to wrap each endpoint in a RequestTimer context manager. 
# The middleware can automatically capture the method, endpoint, and status code 
# for each request and update the appropriate counters and histograms accordingly.
# In short just simplify it
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
