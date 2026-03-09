from deepface import DeepFace
import psycopg2
import pickle
import os
import math

from config import DB_CONFIG


THRESHOLD = 10  # مسافة التشابه


def euclidean_distance(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def register_person(name: str, image_path: str):

    if not os.path.exists(image_path):
        return {"status": "error", "message": "Image not found"}

    try:
        representations = DeepFace.represent(
            img_path=image_path,
            model_name="Facenet",
            enforce_detection=False
        )

        if not representations:
            return {"status": "error", "message": "No face detected"}

        embedding = representations[0]["embedding"]

    except Exception as e:
        return {"status": "error", "message": str(e)}

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # قراءة كل الأشخاص المسجلين
        cur.execute("SELECT id, embedding FROM persons")
        rows = cur.fetchall()

        # مقارنة الـ embedding
        for person_id, db_embedding in rows:
            db_embedding = pickle.loads(db_embedding)

            distance = euclidean_distance(embedding, db_embedding)

            if distance < THRESHOLD:
                cur.close()
                conn.close()

                return {
                    "status": "already_registered",
                    "person_id": person_id
                }

        # لو شخص جديد
        cur.execute(
            "INSERT INTO persons (name, embedding) VALUES (%s, %s) RETURNING id",
            (name, pickle.dumps(embedding))
        )

        person_id = cur.fetchone()[0]

        conn.commit()
        cur.close()
        conn.close()

        return {
            "status": "success",
            "person_id": person_id
        }

    except Exception as e:
        return {"status": "db_error", "message": str(e)}