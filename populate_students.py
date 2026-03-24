import os
import pickle
import psycopg2
from deepface import DeepFace
from config import DB_CONFIG, STUDENT_NAMES

# =====================================
# دالة لحساب embedding من صورة
# =====================================
def get_embedding(image_path):
    try:
        rep = DeepFace.represent(
            img_path=image_path,
            model_name="Facenet",
            enforce_detection=True
        )
        if rep:
            return rep[0]["embedding"]
    except Exception as e:
        print(f"Error processing {image_path}: {e}")

    return None


# =====================================
# الاتصال بقاعدة البيانات
# =====================================
conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

students_dir = os.path.join("data", "students")

print("Starting to populate database...\n")

# =====================================
# loop على كل الطلاب
# =====================================
for student_id, name in STUDENT_NAMES.items():

    # 📁 فولدر الطالب
    student_folder = os.path.join(students_dir, student_id)

    if not os.path.exists(student_folder):
        print(f"❌ Folder not found for {name}")
        continue

    # 📸 هات كل الصور
    files = [f for f in os.listdir(student_folder) if f.lower().endswith(".jpg")]

    if not files:
        print(f"❌ No images found for {name}")
        continue

    # خد أول صورة فقط
    image_path = os.path.join(student_folder, files[0])

    print(f"Processing {name} using {files[0]}...")

    embedding = get_embedding(image_path)

    if embedding is None:
        print(f"❌ Failed to extract embedding for {name}")
        continue

    # تحويل embedding لـ bytes
    embedding_bytes = pickle.dumps(embedding)

    try:
        cur.execute(
            """
            INSERT INTO persons (id, name, embedding)
            VALUES (%s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
            """,
            (student_id, name, embedding_bytes)
        )

        print(f"✅ Added {name}")

    except Exception as e:
        print(f"DB Error for {name}: {e}")

# =====================================
# حفظ التغييرات
# =====================================
conn.commit()
cur.close()
conn.close()

print("\n🔥 All students processed successfully!")