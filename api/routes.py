from fastapi import APIRouter, UploadFile, File, Form
import shutil
import os
import cv2
import time

from core.camera_manager import CameraManager
from core.live_camera import run_live_camera
from core.registration_service import register_person
from core.tracking_engine import detect_and_track
from core.proctoring_engine import detect_phone
from core.face_engine import recognize_face
from core.attendance_service import (
    mark_attendance,
    get_attendance_history,
    get_student_summary
)

router = APIRouter()

TEMP_IMAGE_UPLOAD = "temp/upload.jpg"
TEMP_IMAGE_WEBCAM = "temp/webcam.jpg"

UPLOAD_FOLDER = "temp/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ==========================================
# Upload Image Endpoint
# ==========================================
@router.post("/run")
async def run_attendance(file: UploadFile = File(...)):

    os.makedirs("temp", exist_ok=True)

    with open(TEMP_IMAGE_UPLOAD, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = recognize_face(TEMP_IMAGE_UPLOAD)

    if result["status"] != "recognized":
        return result

    return mark_attendance(
        result["student_id"],
        result["student_name"],
        result["confidence"]
    )


# ==========================================
# Webcam Snapshot Endpoint
# ==========================================
@router.post("/run_webcam")
async def run_webcam():

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        return {"status": "camera_error"}

    time.sleep(1.5)

    best_frame = None

    for _ in range(20):
        ret, frame = cap.read()
        if ret:
            best_frame = frame

    cap.release()

    if best_frame is None:
        return {"status": "capture_failed"}

    best_frame = cv2.cvtColor(best_frame, cv2.COLOR_BGR2RGB)

    os.makedirs("temp", exist_ok=True)
    cv2.imwrite(TEMP_IMAGE_WEBCAM, best_frame)

    result = recognize_face(TEMP_IMAGE_WEBCAM)

    if result["status"] != "recognized":
        return result

    return mark_attendance(
        result["student_id"],
        result["student_name"],
        result["confidence"]
    )


# ==========================================
# Attendance History Endpoint
# ==========================================
@router.get("/attendance/history")
def attendance_history():
    return get_attendance_history()


# ==========================================
# Student Summary Endpoint
# ==========================================
@router.get("/attendance/summary")
def attendance_summary():
    return get_student_summary()


# ==========================================
# Phone Detection Endpoint
# ==========================================
@router.post("/detect_phone")
async def detect_phone_endpoint(file: UploadFile = File(...)):

    os.makedirs("temp", exist_ok=True)

    temp_path = "temp/phone_test.jpg"

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return detect_phone(temp_path)


# ==========================================
# Snapshot Tracking Endpoint
# ==========================================
@router.post("/track_snapshot")
async def track_snapshot(file: UploadFile = File(...)):

    os.makedirs("temp", exist_ok=True)

    temp_path = "temp/track_test.jpg"

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    tracked_objects, recognition_state = detect_and_track(temp_path)

    return {
        "tracked_objects": tracked_objects,
        "recognition_state": recognition_state
    }


# ==========================================
# Register New Person Endpoint
# ==========================================
@router.post("/register-person")
async def register_person_api(
    name: str = Form(...),
    file: UploadFile = File(...)
):

    file_path = f"{UPLOAD_FOLDER}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = register_person(name, file_path)

    return result

@router.get("/live_camera")
def start_live_camera():

    run_live_camera(0)

    return {"status": "camera_started"}

@router.get("/start_campus_cameras")
def start_campus_cameras():

    manager = CameraManager()

    manager.start_camera(0)

    # لو أضفت كاميرات لاحقًا
    # manager.start_camera(1)
    # manager.start_camera(2)

    manager.run()

    return {"status": "campus cameras started"}