from datetime import datetime, date
from sqlalchemy.orm import Session
from sqlalchemy import func

from db.database import SessionLocal
from db import models


# ==========================================
# Mark Attendance (Production Ready)
# ==========================================
def mark_attendance(student_id: str, student_name: str, confidence: float):
    db: Session = SessionLocal()

    try:
        # 1️⃣ تأكد إن الطالب موجود
        student = db.query(models.Student).filter(
            models.Student.student_id == student_id
        ).first()

        if not student:
            student = models.Student(
                student_id=student_id,
                name=student_name
            )
            db.add(student)
            db.commit()

        # 2️⃣ تحقق هل مسجل حضور النهارده
        today = date.today()

        existing_attendance = db.query(models.Attendance).filter(
            models.Attendance.student_id == student_id,
            models.Attendance.date == today
        ).first()

        if existing_attendance:
            return {
                "status": "already_marked",
                "student_id": student_id,
                "student_name": student_name
            }

        # 3️⃣ سجل حضور جديد
        now = datetime.now()

        attendance = models.Attendance(
            student_id=student_id,
            date=today,
            time=now.time(),
            confidence=confidence
        )

        db.add(attendance)
        db.commit()

        return {
            "status": "marked",
            "student_id": student_id,
            "student_name": student_name,
            "confidence": confidence
        }

    except Exception as e:
        print("Attendance Error:", str(e))
        return {"status": "error"}

    finally:
        db.close()


# ==========================================
# Get Attendance History
# ==========================================
def get_attendance_history():
    db: Session = SessionLocal()

    try:
        records = db.query(models.Attendance).all()

        result = []
        for r in records:
            result.append({
                "student_id": r.student_id,
                "date": str(r.date),
                "time": str(r.time),
                "confidence": r.confidence
            })

        return result

    except Exception as e:
        print("History Error:", str(e))
        return {"status": "error"}

    finally:
        db.close()


# ==========================================
# Student Attendance Summary
# ==========================================
def get_student_summary():
    db: Session = SessionLocal()

    try:
        summary = (
            db.query(
                models.Student.student_id,
                models.Student.name,
                func.count(models.Attendance.id).label("total_attendance")
            )
            .outerjoin(
                models.Attendance,
                models.Student.student_id == models.Attendance.student_id
            )
            .group_by(models.Student.student_id, models.Student.name)
            .all()
        )

        result = []
        for row in summary:
            result.append({
                "student_id": row.student_id,
                "student_name": row.name,
                "total_attendance": row.total_attendance
            })

        return result

    except Exception as e:
        print("Summary Error:", str(e))
        return {"status": "error"}

    finally:
        db.close()