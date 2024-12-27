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
from interface.widgets.buttons import option_button
from interface.widgets.text import text
from database.tables import stuff

""" цей віджет використовується виключно для менеджера """


class task_view(QWidget):
    def __init__(self, task: task, parent=None):
        super().__init__(parent)
        self.setFixedHeight(240)
        self.setFixedWidth(195)

        # Застосуємо стиль до всього віджету
        self.setStyleSheet(
            """
            background-color: transparent;
            border-radius: 5px;
            padding: 5px;
            border: 1px solid white;
            """
        )
        self.info = text(f"{task.comment}", 20, "white")
        self.info.setWordWrap(True)
        self.role = text(f"{task.target_role}", 20, "white")
        self.date = text(f"{task.deadline}", 16, "white")

        # Кнопки
        self.button = option_button("Видалити", "rgb(190, 44, 44)")
        self.edit_button = option_button("Редагувати", "blue")

        self.init_ui()
        self.connect_buttons(task)

    def init_ui(self):
        """Ініціалізація інтерфейсу завдання."""
        # Головне вертикальне розташування
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(10, 10, 10, 10)

        # Скрол для перегляду коментаря для задачі
        self.comment_section = QScrollArea()
        self.comment_section.setWidgetResizable(True)
        self.comment_section.setStyleSheet("background: transparent; border: none;")

        # Поміщаємо текст у віджет
        self.comment_widget = QWidget()
        self.comment_layout = QVBoxLayout(self.comment_widget)
        self.comment_layout.addWidget(self.info)
        self.comment_section.setWidget(self.comment_widget)

        self.layout.addWidget(self.comment_section)

        # Розташування для ролі та дати
        self.info_layout = QVBoxLayout()
        self.info_layout.addWidget(self.date, alignment=Qt.AlignLeft)
        self.layout.addLayout(self.info_layout)

        # Нижня панель з кнопками
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.button, alignment=Qt.AlignCenter)
        self.layout.addLayout(self.button_layout)

    def connect_buttons(self, task: task):
        self.button.clicked.connect(lambda: self.delete_task(task))
        self.edit_button.clicked.connect(lambda: self.open_edit_task(task))

    def delete_task(self, task: task):
        from managers.DAO_classes import tasks_DAO
        tasks_DAO.delete_task(task.id)



""" наступний - для стафа, залежно від етапу"""
 

class proccess_task(QWidget):
    def __init__(self, task: task, stuff:stuff ,parent=None):
        super().__init__(parent)
        self.setFixedHeight(240)
        self.setFixedWidth(195)
        self.stuff = stuff
        self.task = task
        # Застосуємо стиль до всього віджету
        self.setStyleSheet(
            """
            background-color: transparent;
            border-radius: 5px;
            padding: 5px;
            border: 1px solid white;
            """
        )
        self.info = text(f"{task.comment}", 20, "white")
        self.info.setWordWrap(True)
        self.date = text(f"{task.deadline}", 16, "white")

        # Кнопки
        self.button = option_button("Видалити", "rgb(39, 109, 150)")

        self.init_ui()
        self.connect_buttons()

    def init_ui(self):
        """Ініціалізація інтерфейсу завдання."""
        # Головне вертикальне розташування
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(10, 10, 10, 10)

        # Скрол для перегляду коментаря для задачі
        self.comment_section = QScrollArea()
        self.comment_section.setWidgetResizable(True)
        self.comment_section.setStyleSheet("background: transparent; border: none;")

        # Поміщаємо текст у віджет
        self.comment_widget = QWidget()
        self.comment_layout = QVBoxLayout(self.comment_widget)
        self.comment_layout.addWidget(self.info)
        self.comment_section.setWidget(self.comment_widget)

        self.layout.addWidget(self.comment_section)

        # Розташування для ролі та дати
        self.info_layout = QVBoxLayout()
        self.info_layout.addWidget(self.date, alignment=Qt.AlignLeft)
        self.layout.addLayout(self.info_layout)

        # Нижня панель з кнопками
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.button, alignment=Qt.AlignCenter)
        self.layout.addLayout(self.button_layout)

    def connect_buttons(self):
        from managers.DAO_classes import tasks_DAO

        self.button.clicked.connect(
            tasks_DAO.to_next_stage(
                self.task,self.stuff
            )
        )
