from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from interface.widgets.buttons import button, icon_button
from interface.widgets.qlines import (
    datepicker,
    email_line,
    parent_line,
    phone_line,
    role_choice,
)
from managers.DAO_classes import roles_DAO
from managers.extra_windows_manager import extra_windows_manager
from managers.resource_path import resource_path


class add_stuff(QMainWindow):
    def __init__(self):
        super().__init__()
        self.back_button = icon_button(
            resource_path.get_path("interface/assets/back_button.png")
        )

        self.surname_line = parent_line("Прізвище")

        self.name_line = parent_line("Імʼя")

        self.role_choice = role_choice(roles_DAO.get_stuff_roles())

        self.phone = phone_line()

        self.adress = parent_line("Адреса")

        self.mail = email_line()

        self.date = datepicker()

        self.add_button = button("Додати")
        self.add_widgets()
        self.connect_buttons()

    def add_widgets(self):
        self.resize(1200, 800)
        self.setMinimumSize(QSize(1000, 600))
        self.setStyleSheet("background-color: rgb(41, 42, 42)")
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

        self.verticalLayoutWidget = QVBoxLayout(self.centralwidget)
        self.verticalLayoutWidget.setSpacing(20)
        self.verticalLayoutWidget.setContentsMargins(20, 60, 20, 60)
        self.verticalLayoutWidget.addWidget(
            self.back_button, alignment=Qt.AlignTop | Qt.AlignLeft
        )
        self.verticalLayoutWidget.addWidget(self.surname_line, alignment=Qt.AlignCenter)
        self.verticalLayoutWidget.addWidget(self.name_line, alignment=Qt.AlignCenter)
        self.verticalLayoutWidget.addWidget(self.role_choice, alignment=Qt.AlignCenter)
        self.verticalLayoutWidget.addWidget(self.phone, alignment=Qt.AlignCenter)
        self.verticalLayoutWidget.addWidget(self.adress, alignment=Qt.AlignCenter)
        self.verticalLayoutWidget.addWidget(self.mail, alignment=Qt.AlignCenter)
        self.verticalLayoutWidget.addWidget(self.date, alignment=Qt.AlignCenter)
        self.verticalLayoutWidget.addWidget(self.add_button, alignment=Qt.AlignCenter)

    def connect_buttons(self):
        self.add_button.clicked.connect(
            lambda: extra_windows_manager.add_stuff(
                name=self.name_line.text().strip(),
                surname=self.surname_line.text().strip(),
                role=self.role_choice.currentText(),
                phone=self.phone.text().strip(),
                address=self.adress.text().strip(),
                email=self.mail.text().strip(),
                birth_date=self.date.date(),
            )
        )
        self.back_button.clicked.connect(self.close)
