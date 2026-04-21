""" 
@file:          services/post_service.py
@description:   CRUD operations for posts
@date:          26 March 2026
@author:        Kalpan Shah
@version:       1.0.0 
"""
# bussiness logic
from typing import List
from datetime import datetime as dt
from datetime import UTC
from uuid import uuid4, UUID
from app.schema.post import Post, PostCreate

# fake db - temp
POSTS_DB = []

# creating post
async def create_post(data: PostCreate) -> Post:
    post = Post(
        id=uuid4(),
        title=data.title,
        content=data.content,
        created_at=dt.now(UTC)
    )

    POSTS_DB.append(post)
    return post

async def get_posts() -> List[Post]:
    print(POSTS_DB)
    return POSTS_DB

async def get_post(post_id: UUID) -> Post | None:
    for post in POSTS_DB:
        if str(post.id) == str(post_id):
            return post
    return None


async def delete_post(post_id: UUID) -> None:
    
    global POSTS_DB
    POSTS_DB = [
        p for p in POSTS_DB if str(p.id) != str(post_id)
    ]

