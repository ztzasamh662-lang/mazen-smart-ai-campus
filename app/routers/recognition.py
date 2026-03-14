from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, date

from app.database import get_db
from app import models
THRESHOLD = 0.8


router = APIRouter(
    prefix="/recognitions",
    tags=["Recognition"]
)


@router.post("/")
def recognize_student(student_name: str, confidence: float, db: Session = Depends(get_db)):

    # 1️⃣ Check confidence threshold
    if confidence < THRESHOLD:
        raise HTTPException(status_code=400, detail="Face not recognized with enough confidence")

    # 2️⃣ Find student by name
    student = db.query(models.Student).filter(
        models.Student.name == student_name
    ).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # 3️⃣ Check if already marked today
    today = date.today()

    existing_attendance = db.query(models.Attendance).filter(
        models.Attendance.student_id == student.id,
        models.Attendance.timestamp >= datetime(today.year, today.month, today.day)
    ).first()

    if existing_attendance:
        return {"message": "Attendance already marked today"}

    # 4️⃣ Create attendance record
    new_attendance = models.Attendance(
        student_id=student.id,
        status="present"
    )

    db.add(new_attendance)
    db.commit()

    return {
        "message": "Attendance marked via recognition",
        "student": student.name,
        "confidence": confidence
    }