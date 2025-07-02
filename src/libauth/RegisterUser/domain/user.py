from sqlalchemy.orm import Session
from ...models.tables import User
from ...messages import UserRegistrationRequest, UserResponse
from passlib.hash import bcrypt
from datetime import datetime

def create_user(db: Session, user_data: UserRegistrationRequest) -> UserResponse:
    
    if user_data.role == "admin" and not user_data.email.endswith("@namshi.com"):
        raise ValueError("Only @namshi.com emails can register as admin.")

    existing_user = db.query(User).filter(
        User.email == user_data.email,
        User.role == user_data.role
    ).first()

    if existing_user:
        raise ValueError(f"{user_data.role.capitalize()} account with this email already exists.")

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
