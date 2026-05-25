"""
@file:          db/session.py
@description:   Database Session Management
@date:          12 May 2026
@last modified:   12 May 2026
@author:        Kalpan Shah
@version:       1.0.0
"""
from typing import AsyncGenerator
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import base_settings, ENV

# Declare the base class for our models
class Base(DeclarativeBase):
    pass

# Create the async engine
engine = create_async_engine(
    base_settings.db_url,
    echo=base_settings.is_dev # Enable SQL query logging for debugging - should be Set to False in production
)

# Create the async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,  # Prevents session from expiring after commit
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides an async database session.
    Yields an AsyncSession and ensures it is properly closed after use.
    """
    async with AsyncSessionLocal() as session:
        yield session
