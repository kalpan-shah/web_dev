""" 
@file:          api/v1/endpoints/posts.py
@description:   API Endpoints for posts
@date:          26 March 2026
@author:        Kalpan Shah
@version:       1.0.0 
"""

from fastapi import APIRouter, HTTPException
from uuid import UUID
from typing import List
from app.schema.post import Post, PostCreate
from app.services import post_service

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/", response_model=Post)
async  def create_post(data: PostCreate):
    return await post_service.create_post(data)

@router.get("/", response_model=List[Post])
async def list_posts():
    return await post_service.get_posts()

@router.get("/{post_id}", response_model=Post)
async def get_post(post_id: UUID):
    # check for post if None raise the relevant exception or return accordingly
    return await post_service.get_post(post_id)

@router.delete("/{post_id}", response_model=Post)
async def remove_post(post_id: UUID):
    # check if post exists and remove
    await post_service.delete_post(post_id)
    return {"status": "deleted"}
