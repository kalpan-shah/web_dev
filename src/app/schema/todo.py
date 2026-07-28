"""
@file:          schema/todo.py
@description:   for data validation - Data Contracts
@date:          26 March 2026
@last modified:   02 July 2026
@author:        Kalpan Shah
@version:       1.0.0
"""

# Imports
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from uuid import UUID

from app.core.enums import TodoStatus


# 1. TodoItems
class TodoItemCreate(BaseModel):
    """
        Create a New Todo Item
    """
    item: str = Field(min_length=1)
    is_checked: bool = False  # Default to unchecked

class TodoItemResponse(TodoItemCreate):
    """
        Todo Item Info Model
    """
    id: UUID
    todo_id: UUID

    model_config = ConfigDict(from_attributes = True)




# 2. Todo
class TodoCreate(BaseModel):
    """
        Create a New Todo
    """
    title: str = ""  # optional
    items: list[TodoItemCreate]  # List of TodoItemCreate objects


class TodoResponse(TodoCreate):
    """
        Todo Info Model
    """
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    skipped_at: datetime | None = None
    completed_at: datetime | None = None
    status: TodoStatus = TodoStatus.pending  # Default status must be 'pending'
    # overide
    items: list[TodoItemResponse]  # List of TodoItem objects

    model_config = ConfigDict(from_attributes = True)


# 3. Update Todo items
class TodoItemUpdate(BaseModel):
    """
        Update an Existing Todo Item
    """
    id: UUID | None = None  # If None, new sub-task
    item: str | None = None  
    is_checked: bool | None = None  
    # Check how will you handle default value for new sub-task, 
    # if id is None, then is_checked should be False by default

# 4. Update Todo
class TodoUpdate(BaseModel):
    """
        Update an Existing Todo
    """
    title: str | None = None  # optional
    status: TodoStatus | None = None  
    # optional, must be one of 'pending', 'completed', 'skipped', 'deleted'
    items: list[TodoItemUpdate] | None = None  
    # optional, list of TodoItemCreate objects
