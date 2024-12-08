from PySide6.QtCore import QCoreApplication, QSize, Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from interface.widgets.buttons import button, icon_button
from interface.widgets.qlines import email_line
from interface.widgets.text import text
from managers.window_manager import window_manager


class forgot_password_page(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1000, 600)
        self.setMinimumSize(QSize(600, 400))
        self.setStyleSheet("background-color: rgb(41, 42, 42)")
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

        self.verticalLayoutWidget = QVBoxLayout(self.centralwidget)
        self.verticalLayoutWidget.setSpacing(30)
        self.verticalLayoutWidget.setContentsMargins(60, 60, 60, 60)

        self.back_button = icon_button("./interface/assets/back_button.png")

        self.label_of_page = text("Відновлення доступу до акаунту", 28, "white")

        self.line_for_mail = email_line()

        self.send_button = button("Надіслати")

        self.add_widgets()
        self.connect_buttons()

    def add_widgets(self):
        self.verticalLayoutWidget.addWidget(
            self.back_button, alignment=Qt.AlignTop | Qt.AlignLeft
        )

        self.verticalLayoutWidget.addWidget(
            self.label_of_page, alignment=Qt.AlignCenter
        )

        self.verticalLayoutWidget.addWidget(
            self.line_for_mail, alignment=Qt.AlignCenter
        )

        self.verticalLayoutWidget.addWidget(self.send_button, alignment=Qt.AlignCenter)

    def connect_buttons(self):
        from managers.mail_manager import mail_manager

        self.send_button.clicked.connect(
            lambda: mail_manager.check_and_send(self.line_for_mail.text())
        )

        from interface.windows.login_page import login_page
        self.back_button.clicked.connect(lambda: window_manager.go_to_page(login_page))