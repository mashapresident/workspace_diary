from typing import List

from PySide6.QtCore import QDate
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDialog,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)


class parent_line(QLineEdit):
    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        self.setFixedSize(800, 40)
        self.setPlaceholderText(text)
        self.setStyleSheet(
            "background-color: rgb(188, 191, 191);\n"
            'font: 20pt "Apple Symbols";\n'
            "color: rgb(146, 108, 230);\n "
            "border-radius: 3px"
        )


class phone_line(parent_line):
    def __init__(self, parent=None):
        super().__init__("+1234567890", parent)
        phone_validator = QRegularExpressionValidator(r"^\+\d*$")
        self.setValidator(phone_validator)


class cost_line(parent_line):
    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        cost_validator = QRegularExpressionValidator(r"\d*$")
        self.setValidator(cost_validator)


class email_line(parent_line):
    def __init__(self, parent=None):
        super().__init__("email@example.com", parent)
        email_validator = QRegularExpressionValidator(
            r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        )
        self.setValidator(email_validator)


class password_line(parent_line):
    def __init__(self, parent=None):
        super().__init__("password", parent)
        self.setEchoMode(QLineEdit.EchoMode.Password)


class check_box(QComboBox):
    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        self.setFixedSize(800, 40)
        self.setPlaceholderText(text)
        self.setStyleSheet(
            "background-color: rgb(188, 191, 191);\n"
            'font: 20pt "Apple Symbols";\n'
            "color: rgb(146, 108, 230);\n "
            "border-radius: 3px"
        )
        self.dialog = None
        # Кнопка для вызова диалога
        self.show_dialog_button = QPushButton(text)
        self.show_dialog_button.clicked.connect(self.show_dialog)

    def show_dialog(self):
        if not self.dialog:
            self.dialog = QDialog()
            self.dialog.setWindowTitle("Dialog Example")
            self.dialog.setFixedSize(300, 150)
        self.dialog.exec()


class groups_choice(check_box):
    from database.tables import groups_list
    def __init__(self, groups: list[groups_list]):
                super().__init__("Група")
                self.dialog = QDialog(self)
                for group in groups:
                    self.addItem(group.name)



class customer_choice(check_box):
    from database.tables import customer
    def __init__(self, customers: list[customer]):
            super().__init__("Замовник")
            self.dialog = QDialog(self)
            for customer in customers:
                self.addItem(customer.fullname)


class role_choice(check_box):
    def __init__(self, roles_list):
        super().__init__("Оберіть роль")
        self.dialog = QDialog(self)

        for role in roles_list:
            self.addItem(role.role)
            
class project_choice(check_box):
    def __init__(self, projects):
        super().__init__("Оберіть роль")
        self.dialog = QDialog(self)

        for project in projects:
            self.addItem(project.name)


class datepicker(QDateEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCalendarPopup(True)
        date = QDate.fromString("01.01.2006", "dd.MM.yyyy")
        self.setDate(date)
        self.setStyleSheet(
            """
            QDateEdit {
                background-color: rgb(161, 149, 189);
                border: 2px solid rgb(98, 90, 143);
                border-radius: 5px;
                font: 15pt "Apple Symbols";
                color: white;
                padding: 2px 10px;
            }
            QDateEdit::drop-down {
                border: none;
            }
        """
        )
        self.setDisplayFormat("dd.MM.yyyy")
