from datetime import datetime

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QVBoxLayout, QWidget

from interface.widgets.buttons import button, icon_button
from interface.widgets.message import message
from interface.widgets.qlines import (
    comment_line,
    datepicker,
    project_choice,
    role_choice,
)
from managers.DAO_classes import project_DAO, roles_DAO, tasks_DAO


class edit_task(QMainWindow):
    def __init__(self, task):
        super().__init__()

        # Зберігаємо завдання
        self.task = task

        # Кнопки
        self.back_button = icon_button("./interface/assets/back_button.png")
        self.add_button = button("Зберегти зміни")

        # Віджети для редагування
        self.project_picker = project_choice(project_DAO.get_all_projects())
        self.role_dropdown = role_choice(roles_DAO.get_stuff_roles())
        self.deadline_picker = datepicker()
        self.comment_input = comment_line("Залиште коментар")

        # Заповнення полів даними завдання
        self.populate_fields()

        # Ініціалізація інтерфейсу
        self.add_widgets()
        self.connect_buttons()

    def populate_fields(self):
        """Заповнює поля форми даними завдання."""
        self.project_picker.setCurrentText(
            project_DAO.get_name_by_id(self.task.project_id)
        )
        self.role_dropdown.setCurrentText(self.task.target_role)

        # Directly use the date from self.task.deadline if it's already a date object
        self.deadline_picker.setDate(self.task.deadline)

        self.comment_input.setText(self.task.comment)

    def add_widgets(self):
        """Додавання віджетів до сторінки."""
        self.resize(1200, 800)
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

        # Додавання елементів до головного макета
        self.layout.addLayout(top_layout)
        self.layout.addWidget(self.project_picker, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.role_dropdown, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.deadline_picker, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.comment_input, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.add_button, alignment=Qt.AlignCenter)

    def connect_buttons(self):
        """Підключення кнопок до відповідних методів."""
        self.add_button.clicked.connect(self.commit_changes)
        self.back_button.clicked.connect(self.close)

    def commit_changes(self):
        """Оновлює завдання в базі даних."""
        # Отримання даних із полів
        target_role = self.role_dropdown.currentText()
        deadline = self.deadline_picker.date().toString("yyyy-MM-dd")
        comment = self.comment_input.toPlainText().strip()
        project_id = project_DAO.get_id_by_name(self.project_picker.currentText())

        # Перевірка заповненості полів
        if not target_role or not project_id or not deadline or not comment:
            message.show_message("Помилка", "Не всі поля заповнені")
            return

        # Перевірка дати
        today = datetime.today().date()
        if datetime.strptime(deadline, "%Y-%m-%d").date() < today:
            message.show_message(
                "Помилка", "Дедлайн не може бути раніше за сьогоднішню дату"
            )
            return

        # Оновлення завдання
        try:
            tasks_DAO.edit_task(
                task_id=self.task.id,
                target_role=target_role,
                project_id=project_id,
                deadline=deadline,
                comment=comment,
            )
            message.show_message("Успіх", "Завдання успішно змінено")
            self.close()
        except Exception as e:
            message.show_message("Помилка", f"Не вдалося змінити завдання: {e}")
