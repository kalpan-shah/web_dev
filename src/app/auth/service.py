"""
@file:          auth/service.py
@description:   Core auth function for users accounts
@date:          20 May 2026
@author:        Kalpan Shah
@version:       1.0.0
"""
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.services import user_service
from app.auth.jwt import sign_jwt, decode_jwt
from app.auth.hashing import verify_password
from app.models.user import User

async def generate_access_token(db: AsyncSession, user_creds: dict) -> dict:
    if user_creds.get("email"):
        _user: User = await user_service.get_user_by_email(db, user_creds["email"])
    elif user_creds.get("username"):
        _user: User = await user_service.get_user_by_username(db, user_creds["username"])
    else:
        raise ValueError("User creds must contain email or username")
    
    if _user is None:
        user_creds.pop("password", "")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with creds: {user_creds} not Found"
        )

    if not verify_password(user_creds.get("password", ""), _user.hashed_pss):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
            # ,headers={} # Crucial for some clients
        )

    # all checks passed
    return sign_jwt(_user.email)

async def get_current_user(db: AsyncSession, token: str) -> User:
    _email = decode_jwt(token)

    if _email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate token"
        )

    return user_service.get_user_by_email(db, _email)
