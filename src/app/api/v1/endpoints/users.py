"""
@file:          api/v1/endpoints/users.py
@description:   API Endpoints to manage users
@date:          19 March 2026
@last modified: 19 May 2026
@author:        Kalpan Shah
@version:       1.0.0
"""

from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schema.user import UserResponse, UserCreate
from app.services import user_service

user_router = APIRouter(prefix="/users", tags=["Users"])

@user_router.post("/", response_model=UserResponse)
async def register_user(data: UserCreate, db: AsyncSession=Depends(get_db)):
    # TODO: add the required data validation and raise error accordingly
    return await user_service.create_new_user(db, data)

@user_router.delete("/{user_id}")
async def delete_user(user_id: UUID, db: AsyncSession=Depends(get_db)):
    return await user_service.delete_user(db, user_id)

@user_router.delete("/")
async def delete_users(user_ids: List[UUID], db: AsyncSession=Depends(get_db)):
    return await user_service.delete_users(db, user_ids)

@user_router.get("/", response_model=List[UserResponse])
async def list_users(db: AsyncSession=Depends(get_db)):
    # TODO: Update the func to do pagination
    return await user_service.get_users(db)

@user_router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: UUID, db: AsyncSession=Depends(get_db)):
    return await user_service.get_user_by_id(db, user_id)
