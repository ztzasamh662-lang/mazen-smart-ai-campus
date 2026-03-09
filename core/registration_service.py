from deepface import DeepFace
import psycopg2
import pickle
import os

from config import DB_CONFIG


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