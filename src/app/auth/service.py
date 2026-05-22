"""
@file:          auth/service.py
@description:   Core auth function for users accounts
@date:          20 May 2026
@author:        Kalpan Shah
@version:       1.0.0
"""
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, Depends, Header
from app.services import user_service
from app.auth.jwt import sign_jwt, decode_jwt
from app.auth.hashing import verify_password
from app.models.user import User
from app.schema.user import UserLogin
from app.db.session import get_db

logger = logging.getLogger("auth")


async def generate_access_token(db: AsyncSession, user_creds: UserLogin) -> dict:
    if user_creds.email:
        _user: User = await user_service.get_user_by_email(db, user_creds.email)
    elif user_creds.username:
        _user: User = await user_service.get_user_by_username(db, user_creds.username)
    else:
        raise ValueError("User creds must contain email or username")

    if _user is None:
        logger.debug(f"User Not Found: {user_creds.email or user_creds.username}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with creds: {user_creds.email or user_creds.username} not Found"
        )

    if not verify_password(user_creds.password or "", _user.hashed_pss):
        logger.debug("Password Verfification Failed")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
            # ,headers={} # Crucial for some clients
        )

    # all checks passed
    return sign_jwt(_user.email)


# region helper function

def get_token(Bearer: str=Header(default=None)): 
    if not Bearer:
        logger.error("Missing Token Bearer")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Token Bearer",
        )

    return Bearer

# endregion

async def get_current_user(db: AsyncSession=Depends(get_db), token: str=Depends(get_token)) -> User:

    _email = decode_jwt(token)

    if _email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate token"
        )

    return await user_service.get_user_by_email(db, _email)


