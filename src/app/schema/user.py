"""
@file:          schema/user.py
@description:   for data validation - Data Contracts
@date:          18 May 2026
@author:        Kalpan Shah
@version:       1.0.0
"""
from typing import Any
from pydantic import BaseModel, EmailStr, Field, model_validator, ConfigDict
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    """
    Shared fields that are safe to expose and common to all User schemas
    """
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    fname: str = ""
    lname: str = ""

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

    model_config = ConfigDict(from_attributes = True)

class UserLogin(BaseModel):
    """Schema for user login"""

    username: str = Field(None, min_length=3, max_length=50)
    email: EmailStr = None
    password: str = Field(..., min_length=8)

    @model_validator(mode="before")
    @classmethod
    def check_username_or_email(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if data.get("username") or data.get("email"):
                return data
        raise ValueError("Either email or username must be provided")

class TokenResponse(BaseModel):
    """
    Schema for successful authentication responses
    """
    access_token: str
    token_type: str = "bearer"
