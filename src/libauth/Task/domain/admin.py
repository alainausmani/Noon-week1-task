from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.libauth.models.TaskTable import Task
from src.libauth.messages import CreateTaskRequest, UpdateTaskRequest
from src.libauth.models.tables import User, UserRole


def get_all_tasks(db: Session):
    return db.query(Task).all()

def get_task_by_id_admin(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
def update_task_admin(db: Session, task_id: int, data: UpdateTaskRequest):
    task = get_task_by_id_admin(db, task_id)

    task.title = data.title
    task.description = data.description
    task.status = data.status

    db.commit()
    db.refresh(task)
    return task

def delete_task_admin(db: Session, task_id: int):
    task = get_task_by_id_admin(db, task_id)
    db.delete(task)
    db.commit()
