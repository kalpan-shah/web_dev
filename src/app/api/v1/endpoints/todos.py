"""
@file:          api/v1/endpoints/todos.py
@description:   API Endpoints for todos
@date:          26 March 2026
@last modified: 29 July 2026
@author:        Kalpan Shah
@version:       1.0.0
"""

from fastapi import APIRouter, HTTPException, Depends, status
from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import UserNotFoundException
from app.core.enums import TodoStatus
from app.core.metrics import RequestTimer
from app.core.metrics import TODO_CREATED, TODO_COMPLETED, TODO_UPDATED, TODO_FETCHED, TODO_DELETED
from app.db.session import get_db
from app.schema.todo import TodoResponse, TodoCreate, TodoUpdate
from app.models.user import User
from app.auth.service import get_current_user
from app.services import todo_service 

todo_router = APIRouter(prefix="/todo", tags=["Todo"])


@todo_router.post("/", response_model=TodoResponse)
async def create_todo(data: TodoCreate, db: AsyncSession=Depends(get_db), user: User=Depends(get_current_user)):
    if not user:
        raise UserNotFoundException()
    
    with RequestTimer(method="POST", endpoint="/todos"):
        _todo = await todo_service.create_todo(db, data, user.id)
        TODO_CREATED.inc()
        return _todo


@todo_router.get("/", response_model=List[TodoResponse])
async def list_todos(db: AsyncSession=Depends(get_db), user: User=Depends(get_current_user)):
    if not user:
        raise UserNotFoundException()
    with RequestTimer(method="GET", endpoint="/todos"):
        _todos = await todo_service.get_all_todo(db, user.id)
        TODO_FETCHED.inc()
        return _todos


@todo_router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(todo_id: UUID, db: AsyncSession=Depends(get_db), user: User=Depends(get_current_user)):
    if not user:
        raise UserNotFoundException()
    # check for todo if None raise the relevant exception or return accordingly
    with RequestTimer(method="GET", endpoint="/todos"):
        _todo = await todo_service.get_todo(db, todo_id, user.id)
        TODO_FETCHED.inc()
        return _todo


@todo_router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_todo(todo_id: UUID, db: AsyncSession=Depends(get_db), user: User=Depends(get_current_user)):
    if not user:
        raise UserNotFoundException()
    # check if todo exists and remove
    with RequestTimer(method="DELETE", endpoint="/todos"):
        success = await todo_service.delete_todo(db, todo_id, user.id)
        if not success:
            TODO_DELETED.labels(status="failure").inc()
            raise HTTPException(status_code=404, detail="Todo not found or could not be deleted")
        TODO_DELETED.labels(status="success").inc()
    return

@todo_router.patch("/{todo_id}", response_model=TodoResponse)
async def update_todo(todo_id: UUID, data: TodoUpdate, db: AsyncSession=Depends(get_db), user: User=Depends(get_current_user)):
    if not user:
        raise UserNotFoundException()
    with RequestTimer(method="PATCH", endpoint="/todos"):
        # check if todo exists and update
        _todo = await todo_service.update_todo(db, todo_id, user.id, data)
        TODO_UPDATED.inc()
        if _todo.status == TodoStatus.completed:
            TODO_COMPLETED.inc()
        return _todo
