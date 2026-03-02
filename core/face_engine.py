import os
from deepface import DeepFace
from config import STUDENTS_DIR, MODEL_NAME, DISTANCE_METRIC, STUDENT_NAMES

CONFIDENCE_THRESHOLD = 0.4


def recognize_face(img_path: str):
    try:
        result = DeepFace.find(
            img_path=img_path,
            db_path=STUDENTS_DIR,
            model_name=MODEL_NAME,
            distance_metric=DISTANCE_METRIC,
            enforce_detection=False,
        )

        if not result or len(result) == 0:
            return {"status": "not_recognized"}

        df = result[0]
        print("\n=== TOP MATCHES ===")
        print(df.head(5))
        print("===================\n")

        if df.empty:
            return {"status": "not_recognized"}

        best_match = df.iloc[0]

        # 🔍 البحث عن عمود المسافة تلقائيًا
        distance_column = None
        for col in best_match.index:
            if "distance" in col.lower() or "cosine" in col.lower():
                distance_column = col
                break

        if distance_column is None:
            raise Exception("Distance column not found")

        distance = float(best_match[distance_column])

        if distance > CONFIDENCE_THRESHOLD:
            return {"status": "not_recognized"}

        identity_path = best_match["identity"]

        student_folder = os.path.basename(os.path.dirname(identity_path))

        student_id = student_folder
        student_name = STUDENT_NAMES.get(student_id, student_id)

        confidence = round(1 - distance, 2)

        return {
            "status": "recognized",
            "student_id": student_id,
            "student_name": student_name,
            "confidence": confidence,
        }

    except Exception as e:
        print("Recognition Error:", str(e))
        return {"status": "error"}