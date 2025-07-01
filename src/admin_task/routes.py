from typing import List
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.shared.db.session import SessionLocal
from src.auth.domain import user as user_service
from src.shared.schemas.task import TaskFileResponse,UpdateTaskRequest, CreateTaskRequest, TaskResponse
from src.admin_task.domain.admin import get_media_for_task
import traceback
from src.auth.token import get_current_user
from src.task.domain.user import (get_media_for_task,create_task_for_user,get_user_tasks,get_task_by_id, update_task_logic,delete_task_logic)
from src.shared.models.TaskTable import Task, TaskStatus
from src.shared.models.tables import User, UserRole
from src.admin_task.domain import admin
from src.task.domain import user
from fastapi import Body

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:  
        db.close()
        
@router.get("/admin/tasks")
def get_all_tasks_for_admin(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)): 
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Access denied")
    return admin.get_all_tasks(db)

@router.get("/admin/tasks/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db), current_user: User =Depends(get_current_user)):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Admin access only")
    return admin.get_task_by_id_admin(db, task_id)

@router.put("/admin/tasks/{task_id}")
def admin_update_task(
    task_id: int,
    data: dict = Body(...),  
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Admins only")
    
    try:
        data_model = UpdateTaskRequest(**data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid data: {str(e)}")
    
    return admin.update_task_admin(db, task_id, data_model)

@router.delete("/admin/tasks/{task_id}")
def admin_delete_task(task_id: int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Admins only")
    admin.delete_task_admin(db, task_id)
    return {"detail": "Task deleted"} 
@router.post("/tasks/{task_id}/upload", response_model=TaskFileResponse)
def upload_file_to_task(task_id: int,file: UploadFile = File(...),db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    if current_user.role == UserRole.admin:
        return admin.upload_file_admin(db, task_id, file)
    else:
        return user.upload_file_user(db, current_user, task_id, file)
    
@router.delete("/tasks/{task_id}/media")
def delete_file(task_id: int, body=Body(...), db=Depends(get_db), current_user=Depends(get_current_user)):
    file_url = body.get("file_url")
    if not file_url:
        raise HTTPException(status_code=400, detail="Missing file_url")
    if current_user.role == UserRole.admin:
        raise HTTPException(status_code=403, detail="Admin deletion not implemented yet")
    else:
        return user.delete_task_file_user(db, current_user, task_id, file_url)

@router.delete("/media/{media_id}")
def delete_file(media_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return user.delete_task_media(db, current_user, media_id)

@router.get("/admin/tasks/{task_id}/media", response_model=List[TaskFileResponse])
def admin_get_task_media(task_id: int, db: Session = Depends(get_db), current_admin: User = Depends(get_current_user)):
    if current_admin.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Admins only")
    return admin.get_media_for_task(db, task_id)
@router.get("/tasks/{task_id}/media", response_model=List[TaskFileResponse])
def get_task_media(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role == UserRole.admin:
        return admin.get_media_for_task(db, task_id)
    return user.get_media_for_task(db, current_user, task_id)
