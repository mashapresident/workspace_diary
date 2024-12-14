from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from database.tables import task
from interface.widgets.text import text
from interface.widgets.buttons import option_button
from interface.windows.extra_windows.page_names import page_names

class task_view(QWidget):
    def __init__(self, task: task, parent=None):
        super().__init__(parent)
        self.setFixedHeight(130)
        self.setFixedWidth(195)

        # Застосуємо стиль до всього віджету
        self.setStyleSheet(
            """
            background-color: transparent;
            border-radius: 5px;
            padding: 10px;
            border: 1px solid white;
            }
            """
        )
        self.info = text(f"{task.comment}", 10, "white")
        self.date = text(f"{task.deadline}", 12, "white")
        
        # Кнопки
        self.delete_button = option_button("Видалити", "red")
        self.edit_button = option_button("Редагувати", "blue")

        self.init_ui()
        self.connect_buttons(task)

    def init_ui(self):
        """Ініціалізація інтерфейсу завдання."""
        # Головне вертикальне розташування
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(10, 10, 10, 10)
        
        # Верхнє розташування для основного тексту завдання
        self.top_layout = QHBoxLayout()
        self.layout.addLayout(self.top_layout)
        
        # Розташування для коментарів та дати
        self.info_layout = QVBoxLayout()
        self.info_layout.addWidget(self.info, alignment=Qt.AlignLeft)
        self.info_layout.addWidget(self.date, alignment=Qt.AlignLeft)
        self.layout.addLayout(self.info_layout)
        
        # Нижня панель з кнопками
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.delete_button, alignment=Qt.AlignRight)
        self.button_layout.addWidget(self.edit_button, alignment=Qt.AlignRight)
        self.layout.addLayout(self.button_layout)

    def connect_buttons(self, task: task):
        from managers.DAO_classes import tasks_DAO
        from managers.window_manager import window_manager
        from interface.windows.extra_windows.edit_task import edit_task

        # Замінимо підключення до кнопок з передачею функцій
        self.delete_button.clicked.connect(lambda: self.delete_task(task))
        self.edit_button.clicked.connect(lambda: self.open_edit_task(task))

    def delete_task(self, task: task):
        from managers.DAO_classes import tasks_DAO
        tasks_DAO.delete_task(task.id)

    def open_edit_task(self, task: task):
        from managers.window_manager import window_manager
        from interface.windows.extra_windows.edit_task import edit_task
        window_manager.open_edit_page(task)
