from fastapi import HTTPException
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from src.libauth.models.tables import User
from src.libauth.messages import UserLoginRequest, LoginResponse
from src.libauth.Loginuser.domain.auth import create_access_token

def login_user(db: Session, credentials: UserLoginRequest) -> LoginResponse:
    user = db.query(User).filter(User.email == credentials.email).first()

    if not user or not bcrypt.verify(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(data={"sub": str(user.id)})

    return LoginResponse(
        access_token=token,
        token_type="bearer",
        expires_in=60 * 1  
    )
