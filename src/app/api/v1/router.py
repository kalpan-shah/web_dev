from fastapi import APIRouter
from app.api.v1.endpoints.todos import todo_router
from app.api.v1.endpoints.users import user_router
from app.core.metrics import REQUEST_COUNT, REQUEST_LATENCY, RequestTimer

api_router = APIRouter()

# Add the todos
api_router.include_router(todo_router)
api_router.include_router(user_router)


@api_router.get("/health")
async def health_check():
    endpoint = "/health"
    method = "GET"
    with RequestTimer(method=method, endpoint=endpoint):
        REQUEST_COUNT.labels(
            method=method, endpoint=endpoint, http_status=200
        ).inc()
        return {
            "status": "probably okay"
        }
