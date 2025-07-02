from typing import List
from src.shared.schemas.task import (
    TaskFileResponse,
    UpdateTaskRequest,
    CreateTaskRequest,
    TaskResponse,
)
import traceback
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, Query
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.task.domain.user import (
    get_media_for_task,
    create_task_for_user,
    get_user_tasks,
    get_task_by_id,
    update_task_logic,
    delete_task_logic,
)
from src.admin_task.domain import admin
from src.task.domain import user
from src.auth.domain import user as user_service
from src.auth.token import get_current_user
from src.shared.db.session import SessionLocal
from src.shared.models.TaskTable import Task, TaskStatus
from src.shared.models.tables import User, UserRole

from fastapi import Body

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/tasks", response_model=TaskResponse)
def create_task(
    request: CreateTaskRequest,
    db=Depends(get_db),
    current_user=Depends(get_current_user),
):
    return create_task_for_user(db, current_user, request)


@router.get("/tasks", response_model=List[TaskResponse])
def list_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Task)
        .filter(Task.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db=Depends(get_db), current_user=Depends(get_current_user)):
    return get_task_by_id(db, current_user, task_id)


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    request: UpdateTaskRequest,
    db=Depends(get_db),
    current_user=Depends(get_current_user),
):
    return update_task_logic(db, current_user, task_id, request)


@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: int, db=Depends(get_db), current_user=Depends(get_current_user)
):
    delete_task_logic(db, current_user, task_id)
    return {"message": "Task deleted successfully"}


@router.post("/tasks/{task_id}/upload", response_model=TaskFileResponse)
def upload_file_to_task(
    task_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role == UserRole.admin:
        return admin.upload_file_admin(db, task_id, file)
    else:
        return user.upload_file_user(db, current_user, task_id, file)
