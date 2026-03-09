import cv2
import os

def save_snapshot(frame, tracking_id, camera_id="cam1"):

    folder = f"snapshots/{camera_id}"
    os.makedirs(folder, exist_ok=True)

    path = f"{folder}/track_{tracking_id}.jpg"

    cv2.imwrite(path, frame)

    return path