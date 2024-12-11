from PySide6.QtCore import QDate, QSize, Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from interface.widgets.buttons import button, icon_button
from interface.widgets.message import message
from interface.widgets.qlines import datepicker, email_line, parent_line, phone_line
from managers.DAO_classes import stuff_DAO


class add_stuff(QMainWindow):
    def __init__(self):
        super().__init__()
        self.back_button = icon_button("./interface/assets/back_button.png")
        
        self.surname_line = parent_line("Прізвище")

        self.name_line = parent_line("Імʼя")

        self.phone = phone_line()

        self.adress = parent_line("Адреса")

        self.mail = email_line()

        self.date = datepicker()

        self.add_button = button("Додати")
        self.add_widgets()
        self.connect_buttons()

    def add_widgets(self):
        self.setWindowTitle("Stuff Registration")
        self.resize(1000, 600)
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
        self.verticalLayoutWidget.addWidget(self.phone, alignment=Qt.AlignCenter)
        self.verticalLayoutWidget.addWidget(self.adress, alignment=Qt.AlignCenter)
        self.verticalLayoutWidget.addWidget(self.mail, alignment=Qt.AlignCenter)
        self.verticalLayoutWidget.addWidget(self.date, alignment=Qt.AlignCenter)
        self.verticalLayoutWidget.addWidget(self.add_button, alignment=Qt.AlignCenter)

    def connect_buttons(self):
        self.add_button.clicked.connect(lambda: self.add_stuff())
        
        from managers.window_manager import window_manager
        from interface.windows.manager_page import manager_page
        self.back_button.clicked.connect(lambda: window_manager.go_to_page(manager_page))

    def add_stuff(self):
        # Retrieve input data
        name = self.name_line.text().strip()
        surname = self.surname_line.text().strip()
        phone = self.phone.text().strip()
        address = self.adress.text().strip()
        email = self.mail.text().strip()
        birth_date = self.date.date().toString(
            "yyyy-MM-dd"
        )  # Use standard format for birth date

        # Check if all required fields are filled
        if not name or not surname or not phone:
            message.show_message("Помилка", "Не всі обовʼязкові поля заповнені")
            return

        # Check if email is valid
        if "@" not in email or "." not in email:
            message.show_message("Помилка", "Некоректний email")
            return

        if stuff_DAO.get_stuff_by_phone(phone):
            message.show_message("Помилка", "Клієнт з таким номером телефона вже існує")
            return
        if stuff_DAO.get_stuff_by_email(email):
            message.show_message("Помилка", "Клієнт з такою поштою вже існує")
            return

        # Check if the customer is over 18
        current_date = QDate.currentDate()
        birth_date_obj = QDate.fromString(birth_date, "yyyy-MM-dd")
        age = current_date.year() - birth_date_obj.year()

        # Adjust age calculation for birthdays that haven't occurred yet this year
        if current_date.month() < birth_date_obj.month() or (
            current_date.month() == birth_date_obj.month()
            and current_date.day() < birth_date_obj.day()
        ):
            age -= 1

        if age < 18:
            message.show_message("Помилка", "Вік має бути 18 років або більше")
            return

        stuff_DAO.add_stuff(
            name,
            surname,
            phone,
            address,
            email,
            birth_date,
        )
