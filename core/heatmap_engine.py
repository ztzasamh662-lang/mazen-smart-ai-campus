import psycopg2
from config import DB_CONFIG
from core.camera_zones import CAMERA_ZONES


def get_heatmap_data():

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        SELECT camera_id, COUNT(*) as activity
        FROM recognition_logs
        GROUP BY camera_id
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    heatmap = []

    for camera_id, count in rows:

        zone = CAMERA_ZONES.get(camera_id, {})

        heatmap.append({
            "camera_id": camera_id,
            "zone_name": zone.get("name"),
            "x": zone.get("x"),
            "y": zone.get("y"),
            "activity": count
        })

    return heatmap