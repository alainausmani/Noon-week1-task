from sqlalchemy import Column, Integer, String, DateTime, Enum, UniqueConstraint, func
from src.shared.db.session import Base
import enum
from sqlalchemy.orm import relationship
from src.shared.models.TaskTable import Task

class UserRole(enum.Enum):
    user = "user"
    admin = "admin"
class User(Base):
    __tablename__ = "users"

    __table_args__ = (
        UniqueConstraint("email", "role", name="uix_email_role"),
    )

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.user)
    created_at = Column(DateTime, default=func.now())
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")