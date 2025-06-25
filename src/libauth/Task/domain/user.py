from sqlalchemy.orm import Session
from src.libauth.models.TaskTable import Task
from src.libauth.messages import CreateTaskRequest, TaskResponse, UpdateTaskRequest
from src.libauth.models.tables import User, UserRole
from fastapi import HTTPException

def create_task_for_user(db: Session, user: User, request: CreateTaskRequest):
    if user.role != UserRole.user:
        raise HTTPException(status_code=403, detail="Only regular users can create tasks.")
    new_task = Task(
        title=request.title,
        description=request.description,
        status=request.status,
        user_id=user.id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def get_user_tasks(db: Session, user: User):
    return db.query(Task).filter(Task.user_id == user.id).all()

def get_task_by_id(db: Session, user: User, task_id: int):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

def update_task_logic(db: Session, user: User, task_id: int, data: UpdateTaskRequest):
    task = get_task_by_id(db, user, task_id)
    task.title = data.title
    task.description = data.description
    task.status = data.status
    db.commit()
    db.refresh(task)
    return task

def delete_task_logic(db: Session, user: User, task_id: int):
    task = get_task_by_id(db, user, task_id)
    db.delete(task)
    db.commit()
