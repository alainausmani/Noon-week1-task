from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Literal
from datetime import datetime
from typing import Optional, List
from enum import Enum


class UserRegistrationRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    role: Literal["user", "admin"]


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    created_at: datetime

    model_config = {"from_attributes": True}


class UserProfileResponse(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str

    model_config = {"from_attributes": True}


class UserUpdateRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
