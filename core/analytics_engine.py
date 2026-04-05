import psycopg2
from config import DB_CONFIG


def get_camera_activity():

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        SELECT camera_id, COUNT(*) as detections
        FROM recognition_logs
        GROUP BY camera_id
        ORDER BY detections DESC
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    data = []

    for camera_id, count in rows:
        data.append({
            "camera_id": camera_id,
            "detections": count
        })

    return data


def get_top_persons(limit=5):

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        SELECT person_id, COUNT(*) as appearances
        FROM recognition_logs
        WHERE person_id IS NOT NULL
        GROUP BY person_id
        ORDER BY appearances DESC
        LIMIT %s
    """, (limit,))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    data = []

    for person_id, count in rows:
        data.append({
            "person_id": person_id,
            "appearances": count
        })

    return data


def get_total_events():

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*) FROM recognition_logs
    """)

    count = cur.fetchone()[0]

    cur.close()
    conn.close()

    return {
        "total_events": count
    }