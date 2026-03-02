import csv
import os
from datetime import datetime
from config import ATTENDANCE_FILE


def initialize_file():
    if not os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["date", "student_id", "student_name"])


def already_marked_today(student_id: str):
    today = datetime.now().strftime("%Y-%m-%d")

    if not os.path.exists(ATTENDANCE_FILE):
        return False

    with open(ATTENDANCE_FILE, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["date"] == today and row["student_id"] == student_id:
                return True

    return False


def mark_attendance(student_id: str, student_name: str):
    today = datetime.now().strftime("%Y-%m-%d")

    with open(ATTENDANCE_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([today, student_id, student_name])