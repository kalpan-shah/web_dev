from sqlalchemy.ext.asyncio import AsyncSession
from app.schema.user import UserCreate
from app.auth.hashing import get_password_hash
from typing import List
from uuid import UUID

async def get_users(db: AsyncSession, offset: int=0, limit:int=10):
    pass

async def get_user_by_email(db: AsyncSession, email: str):
    pass

async def get_user_by_username(db: AsyncSession, username: str):
    pass

async def get_user_by_id(db: AsyncSession, uid: UUID):
    pass

async def create_new_user(db: AsyncSession, user: UserCreate):
    pass

async def delete_users(db: AsyncSession, users: List[UUID]):
    pass

async def delete_user(db: AsyncSession, user_id: UUID):
    pass
