from typing import List
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from shared.schemas.user import UserProfileResponse, UserUpdateRequest
import traceback
from domain.user import get_profile, update_profile
from shared.db.session import SessionLocal
from auth.domain import user as user_service
from auth.jwttoken import get_current_user
from shared.models.tables import User, UserRole


from fastapi import Body

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/profile", response_model=UserProfileResponse)
def read_profile(profile=Depends(get_profile)):
    return profile


@router.put("/profile", response_model=UserProfileResponse)
def modify_profile(update_data: UserUpdateRequest, updated=Depends(update_profile)):
    return updated
