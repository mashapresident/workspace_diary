from datetime import datetime
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QMainWindow, QWidget,
    QComboBox, QLabel, QPushButton, QLineEdit, QTextEdit
)
from interface.widgets.buttons import icon_button, button
from interface.widgets.qlines import datepicker
from managers.DAO_classes import tasks_DAO, role_DAO, project_DAO

class add_task(QMainWindow):
    def __init__(self, project: project_DAO):
        super().__init__()

        # Поля для вводу даних
        self.role_dropdown = QComboBox()
        self.project_id_input = QLineEdit()
        self.deadline_picker = datepicker()
        self.comment_input = QTextEdit()

        # Кнопки
        self.add_button = button("Додати завдання")
        self.back_button = icon_button("./interface/assets/back_button.png")

        
        self.initialize_role_dropdown()
        self.add_widgets()
        self.connect_buttons()

    def initialize_role_dropdown(self):
        """Ініціалізація випадаючого списку ролей."""
        roles = role_DAO.get_roles()
        if roles:
            for role in roles:
                self.role_dropdown.addItem(role.role)

    def add_widgets(self):
        """Додавання віджетів до сторінки."""
        self.resize(600, 400)
        self.setMinimumSize(QSize(600, 400))
        self.setStyleSheet("background-color: rgb(41, 42, 42)")

        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

        self.layout = QVBoxLayout(self.centralwidget)
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(20, 20, 20, 20)

        # Рядок із кнопкою назад
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.back_button, alignment=Qt.AlignLeft)
        self.layout.addLayout(top_layout)

        # Додавання полів
        self.layout.addWidget(QLabel("Оберіть роль:"), alignment=Qt.AlignLeft)
        self.layout.addWidget(self.role_dropdown, alignment=Qt.AlignCenter)

        self.layout.addWidget(QLabel("ID проекту:"), alignment=Qt.AlignLeft)
        self.layout.addWidget(self.project_id_input, alignment=Qt.AlignCenter)

        self.layout.addWidget(QLabel("Дедлайн:"), alignment=Qt.AlignLeft)
        self.layout.addWidget(self.deadline_picker, alignment=Qt.AlignCenter)

        self.layout.addWidget(QLabel("Коментар:"), alignment=Qt.AlignLeft)
        self.layout.addWidget(self.comment_input, alignment=Qt.AlignCenter)


        # Кнопка додавання завдання
        self.layout.addWidget(self.add_button, alignment=Qt.AlignCenter)

    def connect_buttons(self):
        """Підключення кнопок до відповідних методів."""
        self.add_button.clicked.connect(self.add_task)
        self.back_button.clicked.connect(self.close)

    def add_task(self):
        """Додавання нового завдання."""
        from interface.widgets.message import message

        # Отримання даних із полів
        target_role = self.role_dropdown.currentText()
        project_id = self.project_id_input.text().strip()
        deadline = self.deadline_picker.date().toString("yyyy-MM-dd")
        comment = self.comment_input.toPlainText().strip()

        # Перевірка заповненості полів
        if not target_role or not project_id or not deadline  or not comment:
            message.show_message("Помилка", "Не всі поля заповнені")
            return

        # Перевірка дати
        today = datetime.today().date()
        if datetime.strptime(deadline, "%Y-%m-%d").date() < today:
            message.show_message("Помилка", "Дедлайн не може бути раніше за сьогоднішню дату")
            return

        # Додавання завдання
        try:
            tasks_DAO.add_task(
                target_role=target_role,
                project_id=int(project_id),
                deadline=deadline,
                is_done=None,  # Значення за замовчуванням
                is_checked=None,  # Значення за замовчуванням
                comment=comment
            )
            message.show_message("Успіх", "Завдання успішно додано")
            self.close()
        except Exception as e:
            message.show_message("Помилка", f"Не вдалося додати завдання: {e}")
