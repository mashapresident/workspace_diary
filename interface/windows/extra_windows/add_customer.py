from datetime import datetime

from PySide6.QtCore import QSize, Qt
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

from interface.widgets.buttons import button
from interface.widgets.qlines import datepicker, email_line, parent_line, phone_line
from managers.DAO_classes import customer_DAO


class add_customer(QMainWindow):
    def __init__(self):
        super().__init__()
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
        self.setWindowTitle("Customer Registration")
        self.resize(1000, 600)
        self.setMinimumSize(QSize(600, 400))
        self.setStyleSheet("background-color: rgb(41, 42, 42)")
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

        self.verticalLayoutWidget = QVBoxLayout(self.centralwidget)
        self.verticalLayoutWidget.setSpacing(20)
        self.verticalLayoutWidget.setContentsMargins(20, 60, 20, 60)
        self.verticalLayoutWidget.addWidget(self.surname_line, alignment=Qt.AlignCenter)
        self.verticalLayoutWidget.addWidget(self.name_line, alignment=Qt.AlignCenter)
        self.verticalLayoutWidget.addWidget(self.phone, alignment=Qt.AlignCenter)
        self.verticalLayoutWidget.addWidget(self.adress, alignment=Qt.AlignCenter)
        self.verticalLayoutWidget.addWidget(self.mail, alignment=Qt.AlignCenter)
        self.verticalLayoutWidget.addWidget(self.date, alignment=Qt.AlignCenter)
        self.verticalLayoutWidget.addWidget(self.add_button, alignment=Qt.AlignCenter)

    def connect_buttons(self):
        self.add_button.clicked.connect(lambda: self.add_customer())

    def add_customer(self):
        # Получение данных из полей
        name = self.name_line.text().strip()
        surname = self.surname_line.text().strip()
        phone = self.phone.text().strip()
        address = self.adress.text().strip()
        email = self.mail.text().strip()
        birth_date = self.date.date()  # Получаем объект datetime.date

        from interface.widgets.message import message

        # Проверка на заполненность обязательных полей
        if not name or not surname or not phone or not email or not address:
            message.show_message("Помилка", "Не всі поля заповнені")
            return

        # Проверка корректности email
        if "@" not in email or "." not in email:
            message.show_message("Помилка", "Некоректний email")
            return

        if customer_DAO.get_customer_by_phone(phone):
            message.show_message("Помилка", "Клієнт з таким номером телефона вже існує")
            return
        if customer_DAO.get_customer_by_email(email):
            message.show_message("Помилка", "Клієнт з такою поштою вже існує")
            return

        # Проверка возраста клиента
        today = datetime.today().date()
        age = (today - birth_date).days // 365
        if age < 18:
            message.show_message("Помилка", "Клієнт повинен бути старше 18 років")
            return

        customer_DAO.add_customer(
            name,
            surname,
            phone,
            address,
            email,
            birth_date,
        )