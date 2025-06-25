from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from ..context import Base
import enum
from .MediaTable import Media

class TaskStatus(enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.pending, nullable=False)
    created_at = Column(DateTime, default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="tasks")
    media = relationship("Media", back_populates="task", cascade="all, delete-orphan")
