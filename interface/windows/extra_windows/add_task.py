from datetime import datetime
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QMainWindow, QWidget,
    QComboBox, QLabel, QPushButton, QLineEdit, QTextEdit
)
from interface.widgets.buttons import icon_button, button
from interface.widgets.qlines import datepicker, role_choice, parent_line, project_choice
from interface.widgets.text import text
from managers.DAO_classes import tasks_DAO, project_DAO

class add_task(QMainWindow):
    def __init__(self):
        super().__init__()
        self.back_button = icon_button("./interface/assets/back_button.png")
        self.project_picker = project_choice()
        self.role_dropdown = role_choice()
        self.deadline_picker = datepicker()
        self.comment_input = parent_line()

        # Кнопки
        self.add_button = button("Додати завдання")
        self.back_button = icon_button("./interface/assets/back_button.png")

        
        self.add_widgets()
        self.connect_buttons()

   
    def add_widgets(self):
        """Додавання віджетів до сторінки."""
        self.resize(1000, 600)
        self.setMinimumSize(QSize(1000, 600))
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
        
        self.layout.addWidget(text("Оберіть проєкт",14,"white"), alignment=Qt.AlignLeft)
        self.layout.addWidget(self.project_picker, alignment=Qt.AlignCenter)
     
        self.layout.addWidget(text("Оберіть роль",14,"white"), alignment=Qt.AlignLeft)
        self.layout.addWidget(self.role_dropdown, alignment=Qt.AlignCenter)

        self.layout.addWidget(text("Дедлайн",14,"white"), alignment=Qt.AlignLeft)
        self.layout.addWidget(self.deadline_picker, alignment=Qt.AlignCenter)

        self.layout.addWidget(text("Коментар",14,"white"), alignment=Qt.AlignLeft)
        self.layout.addWidget(self.comment_input, alignment=Qt.AlignCenter)

        self.layout.addWidget(self.add_button, alignment=Qt.AlignCenter)

    def connect_buttons(self):
        """Підключення кнопок до відповідних методів."""
        self.add_button.clicked.connect(self.add_task)

    def add_task(self):
        """Додавання нового завдання."""
        from interface.widgets.message import message

        # Отримання даних із полів
        target_role = self.role_dropdown.currentText()
        project_id = self.project_id_input.text().strip()
        deadline = self.deadline_picker.date().toString("yyyy-MM-dd")
        comment = self.comment_input.toPlainText().strip()
        project_id = project_DAO.get_id_by_name(self.project_picker.currentText())

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
                project_id=project_id,
                deadline=deadline,
                comment=comment
            )
            message.show_message("Успіх", "Завдання успішно додано")
            self.close()
        except Exception as e:
            message.show_message("Помилка", f"Не вдалося додати завдання: {e}")
