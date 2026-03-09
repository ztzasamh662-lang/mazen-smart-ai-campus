import psycopg2
from config import DB_CONFIG
from datetime import datetime


def log_recognition(person_id, tracking_id, status, camera_id=1):

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO recognition_logs
            (person_id, tracking_id, status, camera_id, timestamp)
            VALUES (%s,%s,%s,%s,%s)
            """,
            (
                person_id,
                tracking_id,
                status,
                camera_id,
                datetime.utcnow()
            )
        )

        conn.commit()

        cur.close()
        conn.close()

    except Exception as e:

        print("LOG ERROR:", e)