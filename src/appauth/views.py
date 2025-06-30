from typing import List
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.libauth.context import SessionLocal
from src.libauth.messages import TaskFileResponse,UpdateTaskRequest, CreateTaskRequest, TaskResponse, UserUpdateRequest, UserProfileResponse, ResetPasswordRequest, ForgotPasswordRequest, ResetTokenResponse,UserRegistrationRequest, UserResponse, UserLoginRequest, LoginResponse ,UserProfileResponse, UserUpdateRequest
from src.libauth.RegisterUser.domain import user as user_service
from ..libauth.messages import UserLoginRequest, LoginResponse
from src.libauth.Loginuser.domain.user import login_user
from src.libauth.ForgotPassword.domain.user import forgot_password,reset_password
from src.libauth.Task.domain.admin import get_media_for_task
import traceback
from src.libauth.Profile.domain.user import get_profile, update_profile
from src.libauth.Profile.domain.auth import get_current_user
from src.libauth.context import SessionLocal
from src.libauth.models.TaskTable import Task, TaskStatus
from src.libauth.Task.domain.user import (get_media_for_task,create_task_for_user,get_user_tasks,get_task_by_id, update_task_logic,delete_task_logic)
from src.libauth.models.tables import User, UserRole
from src.libauth.Task.domain import admin, user

from fastapi import Body
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:  
        db.close()
        
@router.post("/register", response_model=UserResponse)
def register_user(request: UserRegistrationRequest, db: Session = Depends(get_db)):
    try:
        return user_service.create_user(db, request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        traceback.print_exc()  
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/login", response_model=LoginResponse)
def login(request: UserLoginRequest, db: Session = Depends(get_db)):
    return login_user(db, request)

@router.post("/forgot-password", response_model=ResetTokenResponse)
def forgot_password_endpoint(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    return forgot_password(db, request)

@router.post("/reset-password")
def reset_password_endpoint(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    return reset_password(db, request)

@router.get("/profile", response_model=UserProfileResponse)
def read_profile(profile=Depends(get_profile)):
    return profile

@router.put("/profile", response_model=UserProfileResponse)
def modify_profile(update_data: UserUpdateRequest, updated=Depends(update_profile)):
    return updated

@router.get("/check-role")
def check_existing_roles(email: str, db: Session = Depends(get_db)):
    users = db.query(User).filter(User.email == email).all()
    if not users:
        raise HTTPException(status_code=404, detail="User not found")
    return [u.role.value for u in users]

@router.post("/tasks", response_model=TaskResponse)
def create_task(request: CreateTaskRequest, db=Depends(get_db), current_user=Depends(get_current_user)):
    return create_task_for_user(db, current_user, request)

@router.get("/tasks")
def list_tasks(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return db.query(Task).filter(Task.user_id == current_user.id).all()

@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db=Depends(get_db), current_user=Depends(get_current_user)):
    return get_task_by_id(db, current_user, task_id)

@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, request: UpdateTaskRequest, db=Depends(get_db), current_user=Depends(get_current_user)):
    return update_task_logic(db, current_user, task_id, request)

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db=Depends(get_db), current_user=Depends(get_current_user)):
    delete_task_logic(db, current_user, task_id)
    return {"message": "Task deleted successfully"}

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
