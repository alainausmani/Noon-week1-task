from jose import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from src.shared.models.tables import User, UserRole
from src.shared.schemas.auth import UserLoginRequest, LoginResponse


load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "mysecretkey")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", 60))


def create_access_token(data: dict):
    now = now = datetime.utcnow()
    expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    to_encode.update({"exp": expire , "iat": now})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_token_for_user(user):
    """Call this from user.py after user is fetched."""
    return create_access_token(data={"sub": user.email, "role": user.role.value})



def login_user(db: Session, credentials: UserLoginRequest) -> LoginResponse:
    try:
        selected_role = UserRole(credentials.role)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid role selected.")

    user = db.query(User).filter(
        User.email == credentials.email,
        User.role == selected_role
    ).first()

    if not user or not bcrypt.verify(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_token_for_user(user)

    return LoginResponse(
        access_token=token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES *60
    )