"""
@file:          models/post.py
@description:   Post Model Definition
@date:          14 May 2026
@last modified:   14 May 2026
@author:        Kalpan Shah
@version:       1.0.0
"""
# Mapped - column type, mapped_column - constraints and options
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey, DateTime # Importing necessary SQLAlchemy types
from datetime import datetime as dt
from datetime import timezone
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID # Importing UUID type for PostgreSQL

from app.db.session import Base

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4  # Automatically generate a UUID for new posts
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(String)
    created_at: Mapped[dt] = mapped_column(DateTime, default=dt.now())  # Automatically set the creation time

    def __repr__(self):
        return f"<Post Title={self.title}\n\n>{self.content[:20]}...>"
