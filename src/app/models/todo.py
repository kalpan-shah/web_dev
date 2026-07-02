"""
@file:          models/todo.py
@description:   Todo Model Definition
@date:          14 May 2026
@last modified:   30 June 2026
@author:        Kalpan Shah
@version:       1.0.0
"""
# Mapped - column type, mapped_column - constraints and options
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ARRAY, String, ForeignKey, DateTime, func # Importing necessary SQLAlchemy types
from datetime import datetime as dt
from datetime import timezone
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID # Importing UUID type for PostgreSQL

from app.db.session import Base

class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4  # Automatically generate a UUID for new todos
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=True) # mark as optional
    status: Mapped[str] = mapped_column(String, default="pending")  # Default status is 'pending', other states are 'completed', 'skipped', 'deleted'
    items: Mapped[list["TodoItems"]] = relationship(
        back_populates="todo", 
        cascade="all, delete-orphan",
        passive_deletes=True
    )  # List of TodoItems
    # shall I apply a FK contraint for the above field or does it work
    created_at: Mapped[dt] = mapped_column(DateTime, server_default=func.now())  # Automatically set the creation time
    updated_at: Mapped[dt] = mapped_column(DateTime, nullable=True, onupdate=func.now())  # Automatically update the time on modification
    skipped_at: Mapped[dt] = mapped_column(DateTime, nullable=True)  # Time when the todo was skipped
    completed_at: Mapped[dt] = mapped_column(DateTime, nullable=True)  # Time when the todo was completed
    # marked for deletion, will be deleted after 7 days of last updated

    def __repr__(self):
        if self.title is None:
            item_snippet = self.items[0].item[:20] + "..." if self.items else "Empty"
            return f"<Todo Item snippet={item_snippet}\n\n>{self.status}>"
        return f"<Todo Title={self.title}\n\n>{self.status}>"

class TodoItems(Base):
    __tablename__ = "todo_items"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4  # Automatically generate a UUID for new todo items
    ) 
    todo_id: Mapped[UUID] = mapped_column(ForeignKey("todos.id"), ondelete="CASCADE", nullable=False)  # Foreign key to the parent todo
    item: Mapped[str] = mapped_column(String, nullable=False)  # Each item is a string and cannot be null
    is_checked: Mapped[bool] = mapped_column(default=False)  # Default is unchecked

    # Added for backward child to parent mapping
    todo: Mapped["Todo"] = relationship("Todo", back_populates="items")
