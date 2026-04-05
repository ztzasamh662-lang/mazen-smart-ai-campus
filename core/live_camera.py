import cv2
import numpy as np
import os

from core.tracking_engine import detect_and_track
from core.behavior_engine import detect_loitering, detect_crowd

# Heatmap buffer
heatmap_buffer = np.zeros((720, 1280), dtype=np.float32)


def run_live_camera(camera_id=0):

    global heatmap_buffer

    os.makedirs("temp", exist_ok=True)

    cap = cv2.VideoCapture(camera_id)

    if not cap.isOpened():
        return {"status": "camera_error"}

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame = cv2.resize(frame, (1280, 720))

        # Save frame temporarily
        temp_path = "temp/live_frame.jpg"
        cv2.imwrite(temp_path, frame)

        # Detection + Tracking + Recognition
        tracked_objects, recognition_state = detect_and_track(temp_path)

        # Behavior Detection
        loitering_alerts = detect_loitering(tracked_objects)
        crowd_alert = detect_crowd(tracked_objects)

        for alert in loitering_alerts:
            print("Loitering Alert:", alert)

        if crowd_alert:
            print("Crowd Alert:", crowd_alert)

        # Draw objects
        for obj_id, centroid in tracked_objects.items():

            x, y = centroid
            x = int(x)
            y = int(y)

            label = "Unknown"

            if obj_id in recognition_state:

                state = recognition_state[obj_id]

                if state["status"] == "matched":
                    name = state.get("name", "Person")
                    person_id = state.get("person_id", "")
                    label = f"{name} ({person_id})"

            # Draw point
            cv2.circle(frame, (x, y), 6, (0, 255, 0), -1)

            # Draw label
            cv2.putText(
                frame,
                label,
                (x + 10, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            # Update heatmap
            if 0 <= x < 1280 and 0 <= y < 720:
                heatmap_buffer[y, x] += 1

        # Generate heatmap overlay
        heatmap = cv2.GaussianBlur(heatmap_buffer, (51, 51), 0)

        heatmap_norm = cv2.normalize(
            heatmap,
            None,
            0,
            255,
            cv2.NORM_MINMAX
        )

        heatmap_uint8 = heatmap_norm.astype(np.uint8)

        heatmap_color = cv2.applyColorMap(
            heatmap_uint8,
            cv2.COLORMAP_JET
        )

        overlay = cv2.addWeighted(
            frame,
            0.7,
            heatmap_color,
            0.3,
            0
        )

        cv2.imshow("Smart AI Campus", overlay)

        key = cv2.waitKey(1)

        # ESC to exit
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    return {"status": "camera_stopped"}