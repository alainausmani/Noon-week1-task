from sqlalchemy.orm import Session
from ...models.tables import User
from ...messages import UserRegistrationRequest, UserResponse
from passlib.hash import bcrypt
from datetime import datetime

def create_user(db: Session, user_data: UserRegistrationRequest) -> UserResponse:
    # Check if user with same email exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise ValueError("Email is already registered")

    # Hash the password
    hashed_password = bcrypt.hash(user_data.password)

    # Create new user
    new_user = User(
        email=user_data.email,
        password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        created_at=datetime.utcnow()
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserResponse.from_orm(new_user)
