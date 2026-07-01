"""
@file:          schema/post.py
@description:   for data validation - Data Contracts
@date:          26 March 2026
@author:        Kalpan Shah
@version:       1.0.0
"""

# Imports
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID, uuid4


class TodoCreate(BaseModel):
    """
        Create a New Todo
    """
    title: str
    items: list["TodoItemCreate"]  # List of TodoItemCreate objects


class Todo(TodoCreate):
    """
        Todo Info Model
    """
    id: UUID
    user_id: UUID
    created_at: datetime

class TodoItemCreate(BaseModel):
    """
        Create a New Todo Item
    """
    item: str
    is_checked: bool = False  # Default to unchecked

class TodoUpdate(Todo):
    """
        Update a Todo
    """
    title: str | None = None  # Optional title for update
    items: list["TodoItemUpdate"] | None = None  # Optional list of TodoItemUpdate objects
    