"""
@file:          schema/post.py
@description:   for data validation - Data Contracts
@date:          26 March 2026
@author:        Kalpan Shah
@version:       1.0.0
"""

# Imports
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID, uuid4


class PostCreate(BaseModel):
    """
        Create a New Post
    """
    title: str
    content: str


class Post(PostCreate):
    """
        Post Info Model
    """
    id: UUID
    user_id: UUID
    created_at: datetime
