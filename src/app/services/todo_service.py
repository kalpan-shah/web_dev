"""
@file:          services/todo_service.py
@description:   CRUD operations for todos
@date:          26 March 2026
@last modified: 27 July 2026
@author:        Kalpan Shah
@version:       1.0.0
"""
# bussiness logic
import logging
from typing import List
from datetime import datetime as dt
from datetime import UTC
from uuid import uuid4, UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from app.models.todo import TodoItems, Todo
from app.core.exceptions import UnauthorizedException, TodoNotFoundException
from app.schema.todo import TodoCreate

# Init logger
logger = logging.getLogger("todos")


# creating todo
async def create_todo(db: AsyncSession, data: TodoCreate, user_id: UUID) -> Todo:
    _items = [
        TodoItems(item = item.item, is_checked=item.is_checked)
        for item in data.items
    ]
    todo = Todo(user_id=user_id, title=data.title, items=_items)
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    logger.info(f"Created Todo with ID: {todo.id} for user: {user_id}")
    logger.debug(todo)
    return todo


async def get_all_todo(db: AsyncSession, user_id: UUID) -> List[Todo]:
    logger.debug(f"Retrieving todos for user: {user_id}")
    _stmt = select(Todo).where(Todo.user_id == user_id)
    result = await db.execute(_stmt)
    return result.scalars().all()


async def get_todo(db: AsyncSession, todo_id: UUID, user_id: UUID) -> Todo | None:
    _stmt = select(Todo).where(Todo.id == todo_id).options(selectinload(Todo.items))
    result = await db.execute(_stmt)
    todo = result.scalar_one_or_none()
    if todo is None:
        raise TodoNotFoundException()

    if todo.user_id != user_id:
        logger.warning(f"Unauthorized delete attempt for todo {todo_id} by user {user_id}")
        raise UnauthorizedException()

    return todo


async def delete_todo(db: AsyncSession, todo_id: UUID, user_id: UUID) -> bool:
    await get_todo(db, todo_id, user_id)
    # Above will not raise an exception if todo exists with relevant access
    _stmt = delete(Todo).where(Todo.id == todo_id)
    result = await db.execute(_stmt)
    await db.commit()
    if result.rowcount == 0:
        return False
    logger.info(f"Deleted todo {todo_id} for user {user_id}")
    return True
