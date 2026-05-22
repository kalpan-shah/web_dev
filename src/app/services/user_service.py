"""
@file:          services/user_service.py
@description:   CRUD operations for users
@date:          19 May 2026
@author:        Kalpan Shah
@version:       1.0.0
"""
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.schema.user import UserCreate, UserBase
from app.models.user import User
from app.auth.hashing import get_password_hash
from typing import List
from uuid import UUID
from sqlalchemy import select, delete, update


# Init logger
logger = logging.getLogger("users")
 
async def get_users(db: AsyncSession, offset: int=0, limit:int=10) -> List[User]:
    _stmt = select(User).offset(offset).limit(limit)
    result = await db.execute(_stmt)
    return result.scalars().all()

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    _stmt = select(User).where(User.email == email)
    result = await db.execute(_stmt)
    return result.scalar_one_or_none()

async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    _stmt = select(User).where(User.username == username)
    result = await db.execute(_stmt)
    return result.scalar_one_or_none()

async def get_user_by_id(db: AsyncSession, uid: UUID) -> User | None:
    _stmt = select(User).where(User.id == uid)
    result = await db.execute(_stmt)
    return result.scalar_one_or_none()

async def create_new_user(db: AsyncSession, user: UserCreate) -> User:
    # TODO: check if user already exists by passing the username or email

    # raise relvant exception 
    hashed_pss = get_password_hash(user.password)
    new_user = User(
        username=user.username,
        fname=user.fname,
        lname=user.lname,
        email=user.email,
        hashed_pss=hashed_pss
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    logger.debug("User Created")
    return new_user

async def delete_users(db: AsyncSession, user_ids: List[UUID]) -> int:
    _stmt = delete(User).where(User.id.in_(user_ids))
    result = await db.execute(_stmt)
    await db.commit()
    logger.info(f"Deleted {result.rowcount} Users")

    return result.rowcount

async def delete_user(db: AsyncSession, user_id: UUID) -> bool:
    _stmt = delete(User).where(User.id == user_id)
    result = await db.execute(_stmt)
    await db.commit()
    success = result.rowcount > 0
    if success:
        logger.info(f"Deleted {result.rowcount} User")
    
    return success

async def update_user_info(db: AsyncSession, user_id: UUID, user: UserBase) -> User | None:
    update_data = user.model_dump(exclude_unset=True)
    if not update_data:
        return await get_user_by_id(db, user_id)
    _stmt = update(User).where(User.id == user_id).values(**update_data)
    result = await db.execute(_stmt)
    await db.commit()

    logger.info(f"{result.rowcount} Rows affected")
    if result.rowcount == 0:
        return None

    return await get_user_by_id(db, user_id)
