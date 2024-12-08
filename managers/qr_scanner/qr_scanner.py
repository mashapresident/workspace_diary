import cv2
from PySide6.QtGui import QImage
from pyzbar.pyzbar import decode


class qr_scanner:
    def __init__(self, delay=1, camera_id=0):
        self.camera_id = camera_id
        self.delay = delay
        self.cap = cv2.VideoCapture(self.camera_id)

    def read(self):
        ret, frame = self.cap.read()
        frame = cv2.flip(frame, 1)
        return ret, frame

    def convert_to_image(self, frame):
        "Конвертує кадр з формату BGR (OpenCV) у QImage."

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channels = frame_rgb.shape
        q_image = QImage(frame_rgb.data, width, height, 3 * width, QImage.Format_RGB888)

        return q_image

    def decode_qr(self, frame):
        decoded_objects = decode(frame)
        if decoded_objects:
            return decoded_objects[0].data.decode("utf-8")
        return None

    def release_resources(self):
        if self.cap.isOpened():
            self.cap.release()
