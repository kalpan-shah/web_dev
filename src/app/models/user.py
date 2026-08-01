"""
@file:          models/user.py
@description:   User Model Definition
@date:          18 May 2026
@last modified:   29 July 2026
@author:        Kalpan Shah
@version:       1.0.0
"""
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, DateTime, func # Importing necessary SQLAlchemy types
from datetime import datetime as dt
from datetime import timezone
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID # Importing UUID type for PostgreSQL

from app.db.session import Base
from app.models.todo import Todo

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
    created_at: Mapped[dt] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[dt] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_accessed: Mapped[dt] = mapped_column(DateTime(timezone=True), server_default=func.now())

    todos: Mapped[list["Todo"]] = relationship(
        "Todo",
        # lambda: Todo, 
        # back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True  # Prevents SQLAlchemy from fetching child items into memory before deletion
    )

    def __repr__(self):
        return f"<User username={self.username} email={self.email}>"
