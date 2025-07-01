from sqlalchemy.orm import Session
from src.shared.models.tables import User
from src.shared.schemas.user import UserRegistrationRequest, UserResponse
from passlib.hash import bcrypt
from datetime import datetime
from fastapi import HTTPException, status  

def create_user(db: Session, user_data: UserRegistrationRequest) -> UserResponse:
    user_data.email = user_data.email.lower()

    if user_data.role == "admin" and not user_data.email.endswith("@namshi.com"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only @namshi.com emails can register as admin."
        )

    existing_user = db.query(User).filter(
        User.email == user_data.email,
        User.role == user_data.role
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{user_data.role.capitalize()} account with this email already exists."
        )

    hashed_password = bcrypt.hash(user_data.password)

    new_user = User(
        email=user_data.email,
        password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        role=user_data.role,
        created_at=datetime.utcnow()
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserResponse.from_orm(new_user)
