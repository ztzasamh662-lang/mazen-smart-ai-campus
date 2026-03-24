import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STUDENTS_DIR = os.path.join(BASE_DIR, "data", "students")

MODEL_NAME = "Facenet"
DISTANCE_METRIC = "cosine"

ATTENDANCE_FILE = os.path.join(BASE_DIR, "data", "attendance.csv")

DB_CONFIG = {
    "dbname": "smart_ai",
    "user": "postgres",
    "password": "postgres123",
    "host": "localhost",
    "port": "5432"
}
# 🔥 Mapping ثابت للأسماء
STUDENT_NAMES = {
    "2021001": "Ahmed",
    "2021002": "Baher",
    "2021003": "Islam",
    "2021004": "Mohamed",
    "2021005": "Mazen",
}