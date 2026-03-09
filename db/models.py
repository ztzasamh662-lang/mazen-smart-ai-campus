from sqlalchemy import Column, Integer, String, Float, Date, Time, ForeignKey, UniqueConstraint, Index
from sqlalchemy.sql import func
from sqlalchemy.types import TIMESTAMP
from .database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, unique=True, index=True)
    name = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, ForeignKey("students.student_id"))
    date = Column(Date)
    time = Column(Time)
    confidence = Column(Float)

    # 🔒 منع التكرار في نفس اليوم
    __table_args__ = (
        UniqueConstraint("student_id", "date", name="unique_student_per_day"),
        Index("idx_student_id", "student_id"),
    )