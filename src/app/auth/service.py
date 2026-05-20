"""
@file:          auth/service.py
@description:   Core auth function for users accounts
@date:          20 May 2026
@author:        Kalpan Shah
@version:       1.0.0
"""
from sqlalchemy.ext.asyncio import AsyncSession

from app.services import user_service
from app.auth.jwt import sign_jwt, decode_jwt
from app.models.user import User

async def generate_access_token(db: AsyncSession, user_creds: dict) -> dict:
    # 0. get username/email and password 
    # 1. check if user exist by username or email whichever available,
    #       use user_serivce.get_user_by_[email/username]
    #       raise exception if user not exists
    # 2. if user exists, verify password agains hashed pass
    #       raise exception if verification fails
    # 3. if password verified, generate signed jwt token and return it
    pass

async def get_current_user(db: AsyncSession, token: str) -> User:
    # 1. decode jwt to claim user info - probably uid or email or username
    # 2. based on info get the object
    pass
