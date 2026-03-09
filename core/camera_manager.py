import cv2
from core.tracking_engine import detect_and_track
from core.visualization import draw_boxes


class CameraManager:

    def __init__(self):

        self.cameras = {}

    def start_camera(self, camera_id):

        cap = cv2.VideoCapture(camera_id)

        if not cap.isOpened():

            print("Camera failed:", camera_id)

            return

        self.cameras[camera_id] = cap

        print("Camera started:", camera_id)

    def run(self):

        while True:

            for cam_id, cap in self.cameras.items():

                ret, frame = cap.read()

                if not ret:
                    continue

                temp_path = f"temp/cam_{cam_id}.jpg"

                cv2.imwrite(temp_path, frame)

                tracked, state = detect_and_track(temp_path)

                frame = draw_boxes(frame, tracked, state)

                cv2.imshow(f"Camera {cam_id}", frame)

            key = cv2.waitKey(1)

            if key == 27:
                break

        for cap in self.cameras.values():

            cap.release()

        cv2.destroyAllWindows()