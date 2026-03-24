from deepface import DeepFace
import psycopg2
import pickle
from config import DB_CONFIG
import os
import math


# threshold أدق للتعرف
THRESHOLD = 7


def euclidean_distance(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def recognize_face(image_path):

    if not os.path.exists(image_path):
        return {"status": "error"}

    try:
        # استخراج embedding للشخص الحالي
        representation = DeepFace.represent(
            img_path=image_path,
            model_name="Facenet",
            enforce_detection=False
        )

        if not representation:
            return {"status": "no_face"}

        embedding = representation[0]["embedding"]

    except Exception:
        return {"status": "no_face"}

    # الاتصال بالداتابيز
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("SELECT id, name, embedding FROM persons")
    rows = cur.fetchall()

    for person_id, name, db_embedding in rows:

        db_embedding = pickle.loads(db_embedding)

        # حساب المسافة
        distance = euclidean_distance(embedding, db_embedding)

        if distance < THRESHOLD:

            cur.close()
            conn.close()

            return {
                "status": "matched",
                "person_id": person_id,
                "name": name
            }

    cur.close()
    conn.close()

    return {"status": "unknown"}