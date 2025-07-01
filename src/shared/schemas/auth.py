from pydantic import BaseModel, EmailStr, Field
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from enum import Enum
class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str
    role: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(min_length=8)

class ResetTokenResponse(BaseModel):
    reset_token: str
