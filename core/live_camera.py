import cv2
from core.tracking_engine import detect_and_track
from core.visualization import draw_boxes


def run_live_camera(camera_id=0):

    cap = cv2.VideoCapture(camera_id)

    if not cap.isOpened():
        print("Camera error")
        return

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        temp_path = "temp/live_frame.jpg"

        cv2.imwrite(temp_path, frame)

        tracked_objects, recognition_state = detect_and_track(temp_path)

        frame = draw_boxes(frame, tracked_objects, recognition_state)

        cv2.imshow("Smart AI Campus", frame)

        key = cv2.waitKey(1)

        if key == 27:  # اضغط ESC للخروج
            break

    cap.release()
    cv2.destroyAllWindows()


# هذا الجزء يضمن تشغيل الكاميرا عند تشغيل السكربت
if __name__ == "__main__":
    run_live_camera(1)