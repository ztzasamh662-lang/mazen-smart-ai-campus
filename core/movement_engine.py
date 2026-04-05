import psycopg2
from config import DB_CONFIG


def log_movement(person_id, camera_id):

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO recognition_logs (person_id, camera_id, status)
        VALUES (%s, %s, %s)
    """, (person_id, camera_id, "matched"))

    conn.commit()

    cur.close()
    conn.close()


def get_person_movement(person_id):

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        SELECT camera_id, created_at
        FROM recognition_logs
        WHERE person_id = %s
        ORDER BY created_at ASC
    """, (person_id,))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows