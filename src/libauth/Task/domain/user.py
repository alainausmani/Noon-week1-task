from sqlalchemy.orm import Session
from uuid import uuid4
from src.libauth.models.TaskTable import Task
from src.libauth.messages import CreateTaskRequest, TaskResponse, UpdateTaskRequest
from src.libauth.models.tables import User, UserRole
from fastapi import HTTPException, UploadFile
from src.libauth.models.MediaTable import Media
from fastapi import HTTPException
import os
MEDIA_DIR = "media"

def _save_file_and_record(db: Session, task: Task, file: UploadFile):
    allowed_extensions = [".jpg", ".jpeg", ".png", ".pdf"]
    _, ext = os.path.splitext(file.filename)
    if ext.lower() not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid file type")

    os.makedirs(MEDIA_DIR, exist_ok=True)
    unique_filename = f"{uuid4().hex}_{file.filename}"
    file_path = os.path.join(MEDIA_DIR, unique_filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    media_file = Media(
        task_id=task.id,
        filename=file.filename,
        file_url=f"/media/{unique_filename}"
    )
    db.add(media_file)
    db.commit()
    db.refresh(media_file)
    return media_file


def create_task_for_user(db: Session, user: User, request: CreateTaskRequest):
    if user.role != UserRole.user:
        raise HTTPException(status_code=403, detail="Only regular users can create tasks.")
    existing = db.query(Task).filter(
        Task.user_id == user.id,
        Task.title == request.title
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Task with this title already exists")

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

def get_task_by_id(db, current_user, task_id: int):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()
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

MEDIA_DIR = "media"

def upload_file_user(db: Session, user, task_id: int, file: UploadFile):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return _save_file_and_record(db, task, file)


def delete_task_file_user(db, user, task_id: int, file_url: str):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or not owned by user")
    media = db.query(Media).filter(Media.task_id == task.id, Media.file_url == file_url).first()
    if not media:
        raise HTTPException(status_code=404, detail="Media file not found")
    file_path = file_url.lstrip("/") 
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Failed to remove file: {file_path}", e)
    db.delete(media)
    db.commit()

    return {"detail": "File deleted successfully"}
def get_media_for_task(db: Session, current_user: User, task_id: int):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or not owned by user")

    media_files = db.query(Media).filter(Media.task_id == task_id).all()

    return [
    {
        "id": media.id,
        "filename": media.filename,
        "file_url": media.file_url
    }
    for media in media_files
]
