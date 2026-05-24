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
from app.core.exceptions import UnauthorizedException, PostNotFoundException
from app.schema.post import PostCreate

# Init logger
logger = logging.getLogger("posts")


# creating post
async def create_post(db: AsyncSession, data: PostCreate, user_id: UUID) -> Post:
    post = Post(user_id=user_id, title=data.title, content=data.content)
    db.add(post)
    await db.commit()
    await db.refresh(post)
    logger.info(f"Created post")
    logger.debug(post)
    return post


async def get_posts(db: AsyncSession, user_id: UUID) -> List[Post]:
    logger.debug(f"Retrieving posts")
    _stmt = select(Post).where(Post.user_id == user_id)
    result = await db.execute(_stmt)
    return result.scalars().all()


async def get_post(db: AsyncSession, post_id: UUID, user_id: UUID) -> Post | None:
    _stmt = select(Post).where(Post.id == post_id)
    result = await db.execute(_stmt)
    post = result.scalar_one_or_none()
    if post is None:
        raise PostNotFoundException()

    if post.user_id != user_id:
        logger.warning(f"Unauthorized delete attempt for post {post_id} by user {user_id}")
        raise UnauthorizedException()

    return post


async def delete_post(db: AsyncSession, post_id: UUID, user_id: UUID) -> bool:
    await get_post(db, post_id, user_id)
    # Above will not raise an exception if post exists with relevant access
    _stmt = delete(Post).where(Post.id == post_id)
    result = await db.execute(_stmt)
    await db.commit()
    if result.rowcount == 0:
        return False
    logger.info(f"Deleted post")
    return True
