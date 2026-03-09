import psycopg2
from config import DB_CONFIG


def log_recognition(person_id, tracking_id, status, camera_id="cam1"):

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO recognition_logs (person_id, tracking_id, status, camera_id)
            VALUES (%s, %s, %s, %s)
            """,
            (person_id, tracking_id, status, camera_id)
        )

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        print("Logging error:", e)