import psycopg2
from config import DB_CONFIG


def get_dashboard_stats():

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # total detections
    cur.execute("SELECT COUNT(*) FROM recognition_logs")
    total_events = cur.fetchone()[0]

    # unique persons detected
    cur.execute("""
        SELECT COUNT(DISTINCT person_id)
        FROM recognition_logs
        WHERE person_id IS NOT NULL
    """)
    unique_persons = cur.fetchone()[0]

    # unknown detections
    cur.execute("""
        SELECT COUNT(*)
        FROM recognition_logs
        WHERE status = 'unknown'
    """)
    unknown_count = cur.fetchone()[0]

    cur.close()
    conn.close()

    return {
        "total_events": total_events,
        "unique_persons": unique_persons,
        "unknown_detections": unknown_count
    }


def get_recent_activity(limit=10):

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        SELECT person_id, camera_id, status, created_at
        FROM recognition_logs
        ORDER BY created_at DESC
        LIMIT %s
    """, (limit,))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    activity = []

    for person_id, camera_id, status, created_at in rows:

        activity.append({
            "person_id": person_id,
            "camera_id": camera_id,
            "status": status,
            "time": str(created_at)
        })

    return activity