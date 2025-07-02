from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile
from src.shared.models.TaskTable import Task
from src.shared.schemas.task import CreateTaskRequest, UpdateTaskRequest
from src.shared.models.tables import User, UserRole
import os
from uuid import uuid4
from src.shared.models.MediaTable import Media
from fastapi.responses import JSONResponse

MEDIA_DIR = "media"


def get_media_for_task(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    media_files = db.query(Media).filter(Media.task_id == task_id).all()
    return [
        {"id": media.id, "filename": media.filename, "file_url": media.file_url}
        for media in media_files
    ]


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
        task_id=task.id, filename=file.filename, file_url=f"/media/{unique_filename}"
    )
    db.add(media_file)
    db.commit()
    db.refresh(media_file)
    return media_file


def get_all_tasks(db: Session):
    return db.query(Task).all()


def get_task_by_id_admin(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    media_files = db.query(Media).filter(Media.task_id == task_id).all()

    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "created_at": str(task.created_at),
        "media": [
            {"id": media.id, "filename": media.filename, "file_url": media.file_url}
            for media in media_files
        ],
    }


def update_task_admin(db: Session, task_id: int, data: UpdateTaskRequest):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

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


def upload_file_admin(db: Session, task_id: int, file: UploadFile):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return _save_file_and_record(db, task, file)
