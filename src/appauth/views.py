from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
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


router = APIRouter()

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