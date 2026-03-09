from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
import os

from api.routes import router
from db.database import engine
from db import models

from core.tracking_engine import detect_and_track

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart AI Campus")

app.include_router(router)

# 🔵 Temporary upload folder
UPLOAD_FOLDER = "temp/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.post("/detect")
async def detect(file: UploadFile = File(...)):

    # Save uploaded image temporarily
    file_path = f"{UPLOAD_FOLDER}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run detection + tracking + recognition
    tracked_objects, recognition_state = detect_and_track(file_path)

    return JSONResponse({
        "tracked_objects": tracked_objects,
        "recognition_state": recognition_state
    })