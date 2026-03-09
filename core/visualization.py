import cv2
import psycopg2
from config import DB_CONFIG


def get_person_name(person_id):

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        cur.execute("SELECT name FROM persons WHERE id=%s", (person_id,))
        row = cur.fetchone()

        cur.close()
        conn.close()

        if row:
            return row[0]

        return "Unknown"

    except:
        return "Unknown"


def draw_boxes(frame, detections, recognition_state):

    for obj_id, centroid in detections.items():

        x, y = centroid

        status = recognition_state.get(obj_id, {}).get("status", "unknown")
        person_id = recognition_state.get(obj_id, {}).get("person_id", None)

        if status == "matched" and person_id:

            name = get_person_name(person_id)

            label = f"{name} (ID {person_id})"

            color = (0, 255, 0)

        else:

            label = "Unknown"

            color = (0, 0, 255)

        cv2.circle(frame, (x, y), 6, color, -1)

        cv2.putText(
            frame,
            label,
            (x - 50, y - 15),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2
        )

    return frame