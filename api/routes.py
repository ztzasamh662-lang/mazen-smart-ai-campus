from fastapi import APIRouter, UploadFile, File
import shutil
import os
import cv2

from core.face_engine import recognize_face
from core.attendance_manager import (
    initialize_file,
    already_marked_today,
    mark_attendance,
)

router = APIRouter()

TEMP_IMAGE_UPLOAD = "temp/upload.jpg"
TEMP_IMAGE_WEBCAM = "temp/webcam.jpg"


# ==========================================
# Upload Image Endpoint
# ==========================================
@router.post("/run")
async def run_attendance(file: UploadFile = File(...)):

    os.makedirs("temp", exist_ok=True)

    # Save uploaded image
    with open(TEMP_IMAGE_UPLOAD, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = recognize_face(TEMP_IMAGE_UPLOAD)

    if result["status"] != "recognized":
        return result

    student_id = result["student_id"]
    student_name = result["student_name"]

    initialize_file()

    if already_marked_today(student_id):
        return {
            "status": "already_marked",
            "student_id": student_id,
            "student_name": student_name,
        }

    mark_attendance(student_id, student_name)

    return {
        "status": "marked",
        "student_id": student_id,
        "student_name": student_name,
        "confidence": result["confidence"],
    }


# ==========================================
# Webcam Snapshot Endpoint (Improved)
# ==========================================
@router.post("/run_webcam")
async def run_webcam():

    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        return {"status": "camera_error"}

    # 🔥 استنى 1.5 ثانية عشان الـ auto exposure يظبط
    import time
    time.sleep(1.5)

    best_frame = None

    # خد 20 فريم واختار آخر واحد
    for _ in range(20):
        ret, frame = cap.read()
        if ret:
            best_frame = frame

    cap.release()

    if best_frame is None:
        return {"status": "capture_failed"}

    # تحويل BGR → RGB
    best_frame = cv2.cvtColor(best_frame, cv2.COLOR_BGR2RGB)

    os.makedirs("temp", exist_ok=True)
    cv2.imwrite(TEMP_IMAGE_WEBCAM, best_frame)

    result = recognize_face(TEMP_IMAGE_WEBCAM)

    if result["status"] != "recognized":
        return result

    student_id = result["student_id"]
    student_name = result["student_name"]

    initialize_file()

    if already_marked_today(student_id):
        return {
            "status": "already_marked",
            "student_id": student_id,
            "student_name": student_name,
        }

    mark_attendance(student_id, student_name)

    return {
        "status": "marked",
        "student_id": student_id,
        "student_name": student_name,
        "confidence": result["confidence"],
    }