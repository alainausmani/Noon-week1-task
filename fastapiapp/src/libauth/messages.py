from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# Request body for user registration
class UserRegistrationRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    first_name: str
    last_name: str

# Response body after successful registration
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    created_at: datetime
    model_config = {
        "from_attributes": True
    }
class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

# Login response
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
