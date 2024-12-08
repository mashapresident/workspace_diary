from PySide6.QtCore import QCoreApplication, QSize, Qt, Slot
from PySide6.QtWidgets import QFrame, QMainWindow, QVBoxLayout, QWidget

from interface.widgets.buttons import button, plain_button
from interface.widgets.qlines import email_line, password_line
from interface.widgets.text import text
from interface.windows.forget_password_page import forgot_password_page
from managers.login_manager import login_manager
from managers.qr_manager import qr_manager
from managers.window_manager import window_manager


class login_page(QMainWindow):

    def __init__(self):
        super().__init__()
        self.resize(1000, 600)
        self.setMinimumSize(QSize(600, 400))
        self.setStyleSheet("background-color: rgb(41, 42, 42)")
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

        self.verticalLayoutWidget = QVBoxLayout(self.centralwidget)
        self.verticalLayoutWidget.setSpacing(20)
        self.verticalLayoutWidget.setContentsMargins(0, 60, 0, 60)

        self.label_of_page = text("Вхід у робочий акаунт", 28, "white")

        self.line_for_mail = email_line()

        self.line_for_password = password_line()

        self.enter_button = button("Увійти")

        self.line = QFrame(self.centralwidget)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setStyleSheet("border:20px solid white;")

        self.or_text = text("або", 18, "white")

        self.QRcode_button = button("QR-code")

        self.forget_password_button = plain_button("Я забув пароль")

        self.add_widgets()
        self.connect_buttons()

    def add_widgets(self):
        self.verticalLayoutWidget.addWidget(
            self.label_of_page, alignment=Qt.AlignCenter
        )

        self.verticalLayoutWidget.addWidget(
            self.line_for_mail, alignment=Qt.AlignCenter
        )

        self.verticalLayoutWidget.addWidget(
            self.line_for_password, alignment=Qt.AlignCenter
        )

        self.verticalLayoutWidget.addWidget(self.enter_button, alignment=Qt.AlignCenter)

        self.verticalLayoutWidget.addWidget(self.line)

        self.verticalLayoutWidget.addWidget(self.or_text, alignment=Qt.AlignCenter)

        self.verticalLayoutWidget.addWidget(
            self.QRcode_button, alignment=Qt.AlignCenter
        )

        self.verticalLayoutWidget.addWidget(
            self.forget_password_button, alignment=Qt.AlignCenter
        )

    def connect_buttons(self):
        self.enter_button.clicked.connect(
            lambda: login_manager.login_by_mail(
                self.line_for_mail.text(), self.line_for_password.text()
            )
        )
        self.QRcode_button.clicked.connect(qr_manager.scann_qr_code_from_cam)
        self.forget_password_button.clicked.connect(
            lambda: window_manager.go_to_page(forgot_password_page)
        )

    def closeEvent(self, event):
        window_manager.close_all_active_windows()
        event.accept()
