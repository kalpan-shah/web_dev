"""
@file:          schema/user.py
@description:   for data validation - Data Contracts
@date:          18 May 2026
@author:        Kalpan Shah
@version:       1.0.0
"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    """
    Shared fields that are safe to expose and common to all User schemas
    """
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    fname: str
    lname: str

class UserCreate(UserBase):
    """
    Schema for validating incoming data when creating a new user
    """
    password: str = Field(..., min_length=8)

class UserResponse(UserBase):
    """
    Schema for outgoing user data (Data Contract for API Responses)
    """
    id: UUID
    created_at: datetime
    # last_accessed: datetime | None = None # Uncomment if you want to expose this too

    class Config:
        # Pydantic v2 syntax to allow reading from SQLAlchemy ORM models
        from_attributes = True

class TokenResponse(BaseModel):
    """
    Schema for successful authentication responses
    """
    access_token: str
    token_type: str = "bearer"
