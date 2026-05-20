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
from app.db.session import get_db
from app.schema.post import Post, PostCreate
from app.services import post_service

post_router = APIRouter(prefix="/posts", tags=["Posts"])


@post_router.post("/", response_model=Post)
async def create_post(data: PostCreate, db: AsyncSession=Depends(get_db)):
    return await post_service.create_post(db, data)


@post_router.get("/", response_model=List[Post])
async def list_posts(db: AsyncSession=Depends(get_db)):
    return await post_service.get_posts(db)


@post_router.get("/{post_id}", response_model=Post)
async def get_post(post_id: UUID, db: AsyncSession=Depends(get_db)):
    # check for post if None raise the relevant exception or return accordingly
    return await post_service.get_post(db, post_id)


@post_router.delete("/{post_id}", response_model=Post)
async def remove_post(post_id: UUID, db: AsyncSession=Depends(get_db)):
    # check if post exists and remove
    await post_service.delete_post(db, post_id)
    return {"status": "deleted"}
