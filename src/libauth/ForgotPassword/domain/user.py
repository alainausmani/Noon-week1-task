from fastapi import HTTPException
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from src.libauth.models.tables import User
from src.libauth.messages import ForgotPasswordRequest, ResetPasswordRequest, ResetTokenResponse

SECRET_KEY = "myverysecurekey123"  
ALGORITHM = "HS256"
RESET_TOKEN_EXPIRE_MINUTES = 30

def generate_reset_token(email: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": email, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def forgot_password(db: Session, request: ForgotPasswordRequest) -> ResetTokenResponse:
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    token = generate_reset_token(user.email)
    return ResetTokenResponse(reset_token=token)

def reset_password(db: Session, request: ResetPasswordRequest):
    try:
        payload = jwt.decode(request.token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    hashed_password = bcrypt.hash(request.new_password)
    user.password = hashed_password
    db.commit()
    return {"message": "Password reset successful"}
