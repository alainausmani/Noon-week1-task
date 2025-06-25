from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.libauth.models.tables import User
from src.libauth.context import SessionLocal
from src.libauth.messages import UserRegistrationRequest, UserResponse, UserLoginRequest, LoginResponse ,UserProfileResponse, UserUpdateRequest
from src.libauth.RegisterUser.domain import user as user_service
from ..libauth.messages import UserLoginRequest, LoginResponse
from src.libauth.Loginuser.domain.user import login_user
from src.libauth.messages import ForgotPasswordRequest, ResetTokenResponse
from src.libauth.ForgotPassword.domain.user import forgot_password
from src.libauth.messages import ResetPasswordRequest
from src.libauth.ForgotPassword.domain.user import reset_password
import traceback
from src.libauth.Profile.domain.user import get_profile, update_profile
from src.libauth.messages import UserUpdateRequest, UserProfileResponse
from src.libauth.Profile.domain.auth import get_current_user
from src.libauth.messages import CreateTaskRequest, TaskResponse
from src.libauth.Profile.domain.auth import get_current_user
from src.libauth.context import SessionLocal
from src.libauth.models.TaskTable import Task, TaskStatus
from src.libauth.Task.domain.user import create_task_for_user
from src.libauth.Task.domain.user import (
    get_user_tasks,
    get_task_by_id, update_task_logic,
    delete_task_logic
)
from src.libauth.messages import UpdateTaskRequest

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
    return [u.role.value for u in users]

@router.post("/tasks", response_model=TaskResponse)
def create_task(request: CreateTaskRequest, db=Depends(get_db), current_user=Depends(get_current_user)):
    return create_task_for_user(db, current_user, request)

@router.get("/tasks")
def list_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
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