from collections import defaultdict
import time

# store person presence time
person_presence = defaultdict(lambda: {
    "first_seen": None,
    "last_seen": None
})


LOITERING_THRESHOLD = 10  # seconds
CROWD_THRESHOLD = 5


def detect_loitering(tracked_objects):

    alerts = []

    current_time = time.time()

    for obj_id in tracked_objects:

        record = person_presence[obj_id]

        if record["first_seen"] is None:
            record["first_seen"] = current_time

        record["last_seen"] = current_time

        duration = current_time - record["first_seen"]

        if duration > LOITERING_THRESHOLD:

            alerts.append({
                "type": "loitering",
                "tracking_id": obj_id,
                "duration": duration
            })

    return alerts


def detect_crowd(tracked_objects):

    count = len(tracked_objects)

    if count >= CROWD_THRESHOLD:

        return {
            "type": "crowd_detected",
            "count": count
        }

    return None