"""
@file:          models/user.py
@description:   User Model Definition
@date:          18 May 2026
@last modified:   18 May 2026
@author:        Kalpan Shah
@version:       1.0.0
"""
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, DateTime # Importing necessary SQLAlchemy types
from datetime import datetime as dt
from datetime import timezone
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID # Importing UUID type for PostgreSQL

from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4  # Automatically generate a UUID for new user
    )
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    fname: Mapped[str | None] = mapped_column(String)
    lname: Mapped[str | None] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_pss: Mapped[str] = mapped_column(String)
    created_at: Mapped[dt] = mapped_column(DateTime) # server_default=func.now()
    last_accessed: Mapped[dt | None] = mapped_column(DateTime, nullable=True)

    def __repr__(self):
        return f"<User username={self.username} email={self.email}>"
