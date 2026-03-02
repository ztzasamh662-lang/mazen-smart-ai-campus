from core.face_engine import recognize_face

# غير المسار ده لصورة موجودة عندك
image_path = "data/students/2021005/test.jpg"

result = recognize_face(image_path)

print(result)