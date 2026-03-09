from deepface import DeepFace
import psycopg2
import pickle
from config import DB_CONFIG
import os


def recognize_face(image_path):

    if not os.path.exists(image_path):
        return {"status": "error"}

    try:
        # استخراج embedding للشخص الحالي
        embedding = DeepFace.represent(
            img_path=image_path,
            model_name="Facenet",
            enforce_detection=False
        )[0]["embedding"]

    except Exception:
        return {"status": "no_face"}

    # الاتصال بالداتابيز
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("SELECT id, name, embedding FROM persons")
    rows = cur.fetchall()

    for person_id, name, db_embedding in rows:

        db_embedding = pickle.loads(db_embedding)

        # حساب المسافة (Euclidean)
        distance = sum(
            (a - b) ** 2 for a, b in zip(embedding, db_embedding)
        ) ** 0.5

        if distance < 10:   # threshold مبدئي
            return {
                "status": "matched",
                "person_id": person_id,
                "name": name
            }

    return {"status": "unknown"}