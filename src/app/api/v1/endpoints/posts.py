"""
@file:          api/v1/endpoints/posts.py
@description:   API Endpoints for posts
@date:          26 March 2026
@last modified: 14 May 2026
@author:        Kalpan Shah
@version:       1.0.0
"""

from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import UserNotFoundException
from app.db.session import get_db
from app.schema.post import Post, PostCreate
from app.models.user import User
from app.auth.service import get_current_user
from app.services import post_service

post_router = APIRouter(prefix="/posts", tags=["Posts"])


@post_router.post("/", response_model=Post)
async def create_post(data: PostCreate, db: AsyncSession=Depends(get_db), user: User=Depends(get_current_user)):
    if not user:
        raise UserNotFoundException()
    return await post_service.create_post(db, data, user.id)


@post_router.get("/", response_model=List[Post])
async def list_posts(db: AsyncSession=Depends(get_db), user: User=Depends(get_current_user)):
    if not user:
        raise UserNotFoundException()
    return await post_service.get_posts(db, user.id)


@post_router.get("/{post_id}", response_model=Post)
async def get_post(post_id: UUID, db: AsyncSession=Depends(get_db), user: User=Depends(get_current_user)):
    if not user:
        raise UserNotFoundException()
    # check for post if None raise the relevant exception or return accordingly
    return await post_service.get_post(db, post_id, user.id)


@post_router.delete("/{post_id}", response_model=Post)
async def remove_post(post_id: UUID, db: AsyncSession=Depends(get_db), user: User=Depends(get_current_user)):
    if not user:
        raise UserNotFoundException()
    # check if post exists and remove
    success = await post_service.delete_post(db, post_id, user.id)
    return {"status": "deleted" if success else  "failed to delete"}
