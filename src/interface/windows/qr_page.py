from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import  QPixmap
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class qr_page(QWidget):
    close_page = Signal(bool)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Stream")
        self.resize(300, 200)
        self.setStyleSheet("background-color: rgb(41, 42, 42)")
        self.layout = QVBoxLayout()

        self.video_label = QLabel("Waiting for video...")
        self.video_label.setStyleSheet(
            'font:28px "Apple Symbols";\n' "border: none;\n" "color: white;"
        )
        self.video_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.video_label)
        self.setLayout(self.layout)

    def update_image(self, image):
        self.video_label.setPixmap(QPixmap.fromImage(image))

    def closeEvent(self, event):
        self.close_page.emit(True)
        event.accept()
