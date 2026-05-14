"""
@file:          services/post_service.py
@description:   CRUD operations for posts
@date:          26 March 2026
@author:        Kalpan Shah
@version:       1.0.0
"""
# bussiness logic
import logging
from typing import List
from datetime import datetime as dt
from datetime import UTC
from uuid import uuid4, UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.models.post import Post

from app.schema.post import PostCreate

# Init logger
logger = logging.getLogger("posts")


# creating post
async def create_post(db: AsyncSession,data: PostCreate) -> Post:
    post = Post(**data.model_dump())

    db.add(post)
    await db.commit()
    await db.refresh(post)
    logger.info(f"Created post")
    logger.debug(post)
    return post


async def get_posts(db: AsyncSession) -> List[Post]:
    logger.debug(f"Retrieving posts")
    _stmt = select(Post)
    result = await db.execute(_stmt)
    return result.scalars().all()


async def get_post(db: AsyncSession, post_id: UUID) -> Post | None:
    _stmt = select(Post).where(Post.id == post_id)
    result = await db.execute(_stmt)
    return result.scalar_one_or_none()


async def delete_post(db: AsyncSession,post_id: UUID) -> None:
    _stmt = delete(Post).where(Post.id == post_id)
    await db.execute(_stmt)
    await db.commit()
    logger.info(f"Deleted post")
