from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from enum import Enum


class TaskStatusEnum(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"


class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"


class CreateTaskRequest(BaseModel):
    title: str
    description: str = ""
    status: TaskStatusEnum = TaskStatusEnum.pending


class UpdateTaskRequest(BaseModel):
    title: str
    description: str
    status: TaskStatus

    model_config = {"from_attributes": True}


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

    model_config = {"from_attributes": True}


class TaskFileResponse(BaseModel):
    id: int
    filename: str
    file_url: str

    model_config = {"from_attributes": True}
