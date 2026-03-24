from ultralytics import YOLO
import os

# تحميل موديل YOLOv8 (خفيف وسريع)
model = YOLO("yolov8m.pt")

# Class ID الخاص بالموبايل في COCO dataset
PHONE_CLASS_ID = 67  # cell phone


def detect_phone(image_path: str):

    if not os.path.exists(image_path):
        return {"status": "error", "message": "Image not found"}

    results = model(image_path, imgsz=1280, conf=0.2)

    detected = False
    confidence_score = 0

    for result in results:
        boxes = result.boxes

        if boxes is None:
            continue

        for box in boxes:
            class_id = int(box.cls[0])
            conf = float(box.conf[0])

            print("Detected class:", class_id, "Confidence:", conf)

            if class_id == PHONE_CLASS_ID:
                detected = True
                confidence_score = round(conf, 2)
                break

        if detected:
            break

    if detected:
        return {
            "status": "phone_detected",
            "confidence": confidence_score
        }
    else:
        return {
            "status": "no_phone"
        }