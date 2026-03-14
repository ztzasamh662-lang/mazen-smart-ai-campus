from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app import models

# استيراد الحماية
from app.routers.auth import get_current_user, get_current_admin

router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"]
)

# ===============================
# تسجيل حضور (ADMIN فقط)
# ===============================
@router.post("/mark/{student_id}")
def mark_attendance(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_admin)
):
    # التأكد إن الطالب موجود
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # إنشاء سجل حضور
    new_attendance = models.Attendance(
        student_id=student_id,
        timestamp=datetime.utcnow()
    )

    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)

    return {
        "message": "Attendance marked successfully",
        "student_id": student_id,
        "marked_by": current_user["username"],
        "time": new_attendance.timestamp
    }


# ===============================
# عرض كل سجلات الحضور (أي مستخدم مسجل)
# ===============================
@router.get("/")
def get_all_attendance(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    attendance_records = db.query(models.Attendance).all()
    return attendance_records


# ===============================
# عرض حضور طالب معين (أي مستخدم مسجل)
# ===============================
@router.get("/student/{student_id}")
def get_student_attendance(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    records = db.query(models.Attendance).filter(
        models.Attendance.student_id == student_id
    ).all()

    return records


# ===============================
# Endpoint اختبار الحماية
# ===============================
@router.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {
        "message": "You are authenticated",
        "user": current_user
    }




