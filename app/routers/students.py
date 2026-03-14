from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import models
from app.schemas import StudentCreate

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_students(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()
    return students


@router.post("/")
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    new_student = models.Student(
        name=student.name,
        email=student.email
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student
