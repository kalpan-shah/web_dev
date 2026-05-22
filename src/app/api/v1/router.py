from fastapi import APIRouter
from app.api.v1.endpoints.posts import post_router
from app.api.v1.endpoints.users import user_router

api_router = APIRouter()

# Add the posts
api_router.include_router(post_router)
api_router.include_router(user_router)


@api_router.get("/health")
async def health_check():
    return {
        "status": "probably okay"
    }
