from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QImage

from managers.qr_scanner.qr_scanner import qr_scanner


class qr_scanner_thread(QThread):
    image_received = Signal(QImage)
    qr_data_received = Signal(str)

    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        self.qr_scanner = qr_scanner()
        while self.running:
            ret, frame = self.qr_scanner.read()
            if ret:
                qr_data = self.qr_scanner.decode_qr(frame)
                if qr_data:
                    self.qr_data_received.emit(qr_data)
                    self.running = False
                image = self.qr_scanner.convert_to_image(frame)
                self.image_received.emit(image)

    def stop(self):
        self.running = False
        self.quit()
        self.wait()
        self.qr_scanner.release_resources()
