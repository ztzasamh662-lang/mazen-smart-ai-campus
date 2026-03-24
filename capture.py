import cv2
import time
from datetime import datetime
import csv
from core.recognition_engine import recognize_face  # دالتك الحالية

# =============================
# فتح الكاميرا
# =============================
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
time.sleep(2)  # وقت لتستقر الكاميرا

ret, frame = cap.read()
print("Camera opened:", ret)

if ret:
    # =============================
    # حفظ الصورة مؤقتًا
    # =============================
    temp_path = "temp/live_frame.jpg"
    cv2.imwrite(temp_path, frame)

    # =============================
    # التعرف على الوجه
    # =============================
    result = recognize_face(temp_path)
    print("Raw result from AI:", result)

    if result["status"] == "matched":
        name = result["name"]
        confidence = "N/A"  # الدالة الحالية لا ترجع قيمة ثقة رقمية
        print("Student:", name, "Confidence:", confidence)

        # =============================
        # منع التكرار وحفظ الحضور في CSV
        # =============================
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # التحقق من التكرار
        try:
            with open("attendance.csv", "r") as f:
                rows = f.readlines()
                already_marked = any(name in row for row in rows)
        except FileNotFoundError:
            already_marked = False

        if already_marked:
            print("Status: already_marked")
        else:
            with open("attendance.csv", "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([name, confidence, timestamp])
            print("Status: marked")

    elif result["status"] == "unknown":
        print("Face not recognized")
    else:
        print("Face detection error:", result["status"])

    # =============================
    # عرض الصورة كاختبار
    # =============================
    cv2.imshow("Captured Frame", frame)
    cv2.waitKey(3000)

# =============================
# اغلاق الكاميرا والنوافذ
# =============================
cap.release()
cv2.destroyAllWindows()