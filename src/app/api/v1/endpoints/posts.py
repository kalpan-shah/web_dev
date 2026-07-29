"""
@file:          api/v1/endpoints/posts.py
@description:   API Endpoints for posts
@date:          26 March 2026
@last modified: 27 July 2026
@author:        Kalpan Shah
@version:       1.0.0
"""

from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import UserNotFoundException
from app.db.session import get_db
from app.schema.todo import TodoResponse, TodoCreate, TodoItemResponse, TodoItemCreate
from app.models.user import User
from app.auth.service import get_current_user
from app.services import todo_service 

todo_router = APIRouter(prefix="/todo", tags=["Todo"])


@todo_router.post("/", response_model=TodoResponse)
async def create_todo(data: TodoCreate, db: AsyncSession=Depends(get_db), user: User=Depends(get_current_user)):
    if not user:
        raise UserNotFoundException()
    
    _todo = await todo_service.create_todo(db, data, user.id)

    return await todo_service.get_todo(db, _todo.id, user.id)



@todo_router.get("/", response_model=List[TodoResponse])
async def list_todos(db: AsyncSession=Depends(get_db), user: User=Depends(get_current_user)):
    if not user:
        raise UserNotFoundException()
    return await todo_service.get_all_todo(db, user.id)


@todo_router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(todo_id: UUID, db: AsyncSession=Depends(get_db), user: User=Depends(get_current_user)):
    if not user:
        raise UserNotFoundException()
    # check for todo if None raise the relevant exception or return accordingly
    return await todo_service.get_todo(db, todo_id, user.id)


@todo_router.delete("/{todo_id}")
async def remove_todo(todo_id: UUID, db: AsyncSession=Depends(get_db), user: User=Depends(get_current_user)):
    if not user:
        raise UserNotFoundException()
    # check if todo exists and remove
    success = await todo_service.delete_todo(db, todo_id, user.id)
    return {"status": "deleted" if success else  "failed to delete"}
