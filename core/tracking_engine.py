import numpy as np
import cv2
import time
from ultralytics import YOLO

from core.movement_engine import log_movement
from core.logging_service import log_recognition
from core.snapshot_manager import save_snapshot
from core.recognition_engine import recognize_face
from core.identity_cache import store_identity, get_identity
from api.alert_service import send_alert


face_model = YOLO("yolov8n.pt")

PERSON_CLASS_ID = 0


class SimpleTracker:
    def __init__(self, distance_threshold=100):

        self.next_id = 1
        self.objects = {}
        self.distance_threshold = distance_threshold

        self.recognition_state = {}

        # NEW
        self.frame_count = 0
        self.recheck_interval = 10

    def _get_centroid(self, box):

        x1, y1, x2, y2 = box
        return int((x1 + x2) / 2), int((y1 + y2) / 2)

    def update(self, detections, frame):

        self.frame_count += 1

        updated_objects = {}

        for box in detections:

            centroid = self._get_centroid(box)

            assigned = False

            for obj_id, prev_centroid in self.objects.items():

                distance = np.linalg.norm(
                    np.array(centroid) - np.array(prev_centroid)
                )

                if distance < self.distance_threshold:

                    updated_objects[obj_id] = centroid
                    assigned = True
                    break

            if not assigned:

                obj_id = self.next_id
                updated_objects[obj_id] = centroid
                self.next_id += 1

                self.recognition_state[obj_id] = {
                    "status": "pending",
                    "person_id": None
                }

                snapshot_path = save_snapshot(frame, obj_id)

                result = recognize_face(snapshot_path)

                if result["status"] == "matched":
                    self.recognition_state[obj_id]["status"] = "matched"
                    self.recognition_state[obj_id]["person_id"] = result["person_id"]
                    self.recognition_state[obj_id]["name"] = result["name"]

                    log_movement(result["person_id"], camera_id=1)
                    
                    store_identity(obj_id, result["person_id"], time.time())

                    log_recognition(
                        person_id=result["person_id"],
                        tracking_id=obj_id,
                        status="matched"
                    )

                else:

                    self.recognition_state[obj_id]["status"] = "unknown"

                    log_recognition(
                        person_id=None,
                        tracking_id=obj_id,
                        status="unknown"
                    )

                    send_alert(f"Unknown person detected - Track {obj_id}")

            else:

                # RECHECK every few frames
                if self.frame_count % self.recheck_interval == 0:

                    snapshot_path = save_snapshot(frame, obj_id)

                    result = recognize_face(snapshot_path)

                    if result["status"] == "matched":

                        self.recognition_state[obj_id]["status"] = "matched"
                        self.recognition_state[obj_id]["person_id"] = result["person_id"]

        self.objects = updated_objects

        return self.objects, self.recognition_state


tracker = SimpleTracker()


def detect_and_track(image_path: str):

    frame = cv2.imread(image_path)

    results = face_model(image_path, imgsz=640)

    detections = []

    for result in results:

        boxes = result.boxes

        if boxes is None:
            continue

        for box in boxes:

            class_id = int(box.cls[0])

            if class_id == PERSON_CLASS_ID:

                x1, y1, x2, y2 = box.xyxy[0].tolist()

                detections.append((x1, y1, x2, y2))

    tracked_objects, recognition_state = tracker.update(detections, frame)

    return tracked_objects, recognition_state