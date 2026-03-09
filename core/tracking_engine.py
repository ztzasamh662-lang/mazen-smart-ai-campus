import numpy as np
import cv2
from ultralytics import YOLO

from core.logging_service import log_recognition
from core.snapshot_manager import save_snapshot
from core.recognition_engine import recognize_face
from api.alert_service import send_alert


# YOLO Model
face_model = YOLO("yolov8n.pt")

PERSON_CLASS_ID = 0  # class id for person


class SimpleTracker:
    def __init__(self, distance_threshold=100):
        self.next_id = 1
        self.objects = {}  # tracking_id -> centroid
        self.distance_threshold = distance_threshold

        # recognition state per tracking_id
        self.recognition_state = {}  # tracking_id -> {status, person_id}

    def _get_centroid(self, box):
        x1, y1, x2, y2 = box
        return int((x1 + x2) / 2), int((y1 + y2) / 2)

    def update(self, detections, frame):
        """
        detections: list of bounding boxes [(x1,y1,x2,y2), ...]
        frame: current video frame (numpy array)
        """

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
                # New object detected
                obj_id = self.next_id
                updated_objects[obj_id] = centroid
                self.next_id += 1

                # Initialize recognition state
                self.recognition_state[obj_id] = {
                    "status": "pending",
                    "person_id": None
                }

                # Take snapshot
                snapshot_path = save_snapshot(frame, obj_id)

                # Run recognition
                result = recognize_face(snapshot_path)

                # ===== MATCHED =====
                if result["status"] == "matched":

                    self.recognition_state[obj_id]["status"] = "matched"
                    self.recognition_state[obj_id]["person_id"] = result["person_id"]

                    # Log to database
                    log_recognition(
                        person_id=result["person_id"],
                        tracking_id=obj_id,
                        status="matched"
                    )

                # ===== UNKNOWN =====
                else:

                    self.recognition_state[obj_id]["status"] = "unknown"

                    # Log to database
                    log_recognition(
                        person_id=None,
                        tracking_id=obj_id,
                        status="unknown"
                    )

                    # Send alert
                    send_alert(f"Unknown person detected - Track {obj_id}")

        self.objects = updated_objects

        return self.objects, self.recognition_state


# Global tracker instance
tracker = SimpleTracker()


def detect_and_track(image_path: str):
    """
    image_path: path to image frame
    """

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