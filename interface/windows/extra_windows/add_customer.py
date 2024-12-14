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

from interface.widgets.buttons import button, icon_button
from interface.widgets.qlines import datepicker, email_line, parent_line, phone_line
from managers.DAO_classes import customer_DAO


class add_customer(QMainWindow):
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
        self.verticalLayoutWidget.addWidget(self.phone, alignment=Qt.AlignCenter)
        self.verticalLayoutWidget.addWidget(self.adress, alignment=Qt.AlignCenter)
        self.verticalLayoutWidget.addWidget(self.mail, alignment=Qt.AlignCenter)
        self.verticalLayoutWidget.addWidget(self.date, alignment=Qt.AlignCenter)
        self.verticalLayoutWidget.addWidget(self.add_button, alignment=Qt.AlignCenter)

    def connect_buttons(self):
        self.add_button.clicked.connect(self.add_customer)
        self.back_button.clicked.connect(self.close)

    
    def add_customer(self):
        # Получение данных из полей
        name = self.name_line.text().strip()
        surname = self.surname_line.text().strip()
        phone = self.phone.text().strip()
        address = self.adress.text().strip()
        email = self.mail.text().strip()
        birth_date = self.date.date().toPython()  # Convert QDate to datetime.date

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

        # Перетворення birth_date у строку у форматі 'YYYY-MM-DD'
        birth_date_str = birth_date.strftime('%Y-%m-%d')

        # Обчислення віку
        birth_date_obj = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
        age = (today - birth_date_obj).days // 365
        if age < 18:
            message.show_message("Помилка", "Клієнт повинен бути старше 18 років")
            return

        # Виклик add_customer з рядковим форматом дати
        customer_DAO.add_customer(
            name,
            surname,
            phone,
            address,
            email,
            birth_date_str,  # Передаємо дату як строку у форматі 'YYYY-MM-DD'
        )
        message.show_message("Успішно", "Клієнта зареєстровано")