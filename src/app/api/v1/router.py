from fastapi import APIRouter
from app.api.v1.endpoints import posts

api_router = APIRouter()

# Add the posts
api_router.include_router(posts.router)


@api_router.get("/health")
async def health_check():
    return {
        "status": "probably okay"
    }
