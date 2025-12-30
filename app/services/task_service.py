from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate

class TaskService:
    @staticmethod
    def create_task(db: Session, task_data: TaskCreate) -> Task:
        db_task = Task(
            title=task_data.title,
            description=task_data.description,
            status=task_data.status
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def get_task_by_id(db: Session, task_id: int) -> Task:
        return db.query(Task).filter(Task.id == task_id).first()

    @staticmethod
    def get_all_tasks(db: Session, page: int = 1, page_size: int = 10) -> dict:
        skip = (page - 1) * page_size
        total = db.query(func.count(Task.id)).scalar()
        tasks = db.query(Task).offset(skip).limit(page_size).all()
        total_pages = (total + page_size - 1) // page_size
        
        return {
            "items": tasks,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages
        }

    @staticmethod
    def update_task(db: Session, task_id: int, task_data: TaskUpdate) -> Task:
        db_task = db.query(Task).filter(Task.id == task_id).first()
        if db_task:
            update_data = task_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_task, field, value)
            db.commit()
            db.refresh(db_task)
        return db_task

    @staticmethod
    def delete_task(db: Session, task_id: int) -> bool:
        db_task = db.query(Task).filter(Task.id == task_id).first()
        if db_task:
            db.delete(db_task)
            db.commit()
            return True
        return False
