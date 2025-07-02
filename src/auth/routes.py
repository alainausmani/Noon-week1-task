from typing import List
import traceback
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.shared.db.session import SessionLocal
from src.auth.domain import user as user_service
from src.shared.schemas.auth import UserLoginRequest, LoginResponse
from src.auth.domain.auth import login_user
from src.auth.domain.password import forgot_password, reset_password
from src.auth.token import get_current_user
from src.shared.models.TaskTable import Task, TaskStatus
from src.shared.models.tables import User, UserRole
from src.shared.schemas.auth import (
    ResetPasswordRequest,
    ForgotPasswordRequest,
    ResetTokenResponse,
)
from src.shared.schemas.user import UserResponse, UserRegistrationRequest


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
def forgot_password_endpoint(
    request: ForgotPasswordRequest, db: Session = Depends(get_db)
):
    return forgot_password(db, request)


@router.post("/reset-password")
def reset_password_endpoint(
    request: ResetPasswordRequest, db: Session = Depends(get_db)
):
    return reset_password(db, request)
