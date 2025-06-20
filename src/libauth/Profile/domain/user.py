from fastapi import Depends
from sqlalchemy.orm import Session
from src.libauth.models.tables import User
from src.libauth.messages import UserProfileResponse, UserUpdateRequest
from src.libauth.Profile.domain.auth import get_current_user, get_db

def get_profile(current_user : User = Depends (get_current_user))-> UserProfileResponse:
    return UserProfileResponse.from_orm(current_user)

def update_profile(
        update_data: UserUpdateRequest,
        db : Session=Depends(get_db),
        current_user: User = Depends(get_current_user)
)-> UserProfileResponse:
    if update_data.first_name:
        current_user.first_name=update_data.first_name
    if update_data.last_name:
        current_user.last_name=update_data.last_name
    db.commit()
    db.refresh(current_user)

    return UserProfileResponse.from_orm(current_user)
