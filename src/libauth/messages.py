from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Literal, Optional
from enum import Enum
from typing import List

class TaskStatusEnum(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"

class CreateTaskRequest(BaseModel):
    title: str
    description: str = ""
    status: TaskStatusEnum = TaskStatusEnum.pending
class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"

class UpdateTaskRequest(BaseModel):
    title: str
    description: str
    status: TaskStatus
    model_config = {
        "from_attributes": True
    }
  
    

class MediaInfo(BaseModel):
    filename: str
    file_url: str

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    created_at: datetime
    media: List[MediaInfo] = []
    model_config = {
        "from_attributes": True
    }
  

class TaskFileResponse(BaseModel):
    id: int
    filename: str
    file_url: str
    model_config = {
        "from_attributes": True
    }

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
    model_config = {
        "from_attributes": True
    }
    
class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str
    role : str

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

class UserProfileResponse(BaseModel):
    email:EmailStr
    first_name:str
    last_name:str
    model_config={
        "from_attributes":True
    }

class UserUpdateRequest(BaseModel):
    first_name:Optional[str]=None
    last_name:Optional[str]=None