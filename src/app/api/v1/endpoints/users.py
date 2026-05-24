"""
@file:          api/v1/endpoints/users.py
@description:   API Endpoints to manage users
@date:          19 March 2026
@last modified: 20 May 2026
@author:        Kalpan Shah
@version:       1.0.0
"""
import logging
from fastapi import APIRouter, Depends
from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import UserNotFoundException
from app.db.session import get_db
from app.models.user import User
from app.schema.user import UserResponse, UserCreate, UserLogin
from app.services import user_service
from app.auth.service import generate_access_token, get_current_user


logger = logging.getLogger("users")

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post("/", response_model=UserResponse)
async def register_user(data: UserCreate, db: AsyncSession=Depends(get_db), user: User=Depends(get_current_user)):
    # for now just check if user_exists and if yes they'll add another user
    if not user:
        raise UserNotFoundException()

    return await user_service.create_new_user(db, data)

@user_router.delete("/{user_id}")
async def delete_user(user_id: UUID, db: AsyncSession=Depends(get_db), user: User=Depends(get_current_user)):
    if not user:
        raise UserNotFoundException()
    return await user_service.delete_user(db, user_id)

@user_router.delete("/")
async def delete_users(user_ids: List[UUID], db: AsyncSession=Depends(get_db), user: User=Depends(get_current_user)):
    if not user:
        raise UserNotFoundException()
    return await user_service.delete_users(db, user_ids)

@user_router.get("/", response_model=List[UserResponse])
async def list_users(db: AsyncSession=Depends(get_db), user: User=Depends(get_current_user)):
    if not user:
        raise UserNotFoundException()
    # TODO: Update the func to do pagination
    return await user_service.get_users(db)

@user_router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: UUID, db: AsyncSession=Depends(get_db), user: User=Depends(get_current_user)):
    if not user:        # TODO: add the required data validation and raise error accordingly
        raise UserNotFoundException()
    return await user_service.get_user_by_id(db, user_id)

@user_router.post("/token")
async def get_access_token(user_creds: UserLogin, db: AsyncSession=Depends(get_db)):

    return await generate_access_token(db, user_creds)
