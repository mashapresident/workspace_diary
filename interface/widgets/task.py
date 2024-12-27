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
from database.tables import stuff, task as TaskBase
from database.tables import task
from interface.widgets.text import text
from interface.widgets.buttons import option_button
from managers.DAO_classes import tasks_DAO
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
        self.delete_button = option_button("Видалити", "rgb(190, 44, 44)")
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
        self.info_layout.addWidget(self.role, alignment=Qt.AlignLeft)
        self.info_layout.addWidget(self.date, alignment=Qt.AlignLeft)
        self.layout.addLayout(self.info_layout)

        # Нижня панель з кнопками
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.delete_button, alignment=Qt.AlignRight)
        self.button_layout.addWidget(self.edit_button, alignment=Qt.AlignRight)
        self.layout.addLayout(self.button_layout)

    def connect_buttons(self, task: task):
        self.delete_button.clicked.connect(lambda: self.delete_task(task))
        self.edit_button.clicked.connect(lambda: self.open_edit_task(task))

    def delete_task(self, task: task):
        from managers.DAO_classes import tasks_DAO
        tasks_DAO.delete_task(task.id)

    def open_edit_task(self, task: task):
        from managers.window_manager import window_manager
        window_manager.open_edit_page(task)

""" наступні віджети - для стафа, залежно від етапу"""
class task_base(QWidget):
    def __init__(self, task: TaskBase, parent=None):
        super().__init__(parent)
        self.task = task
        self.setFixedHeight(240)
        self.setFixedWidth(195)
        self.setStyleSheet(
            """
            background-color: transparent;
            border-radius: 5px;
            padding: 5px;
            border: 1px solid white;
            """
        )
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(10, 10, 10, 10)

    def init_ui(self):
        raise NotImplementedError("Subclasses must implement this method")

    def connect_buttons(self):
        raise NotImplementedError("Subclasses must implement this method")


class given_task(task_base):
    def __init__(self, task: TaskBase, parent=None):
        super().__init__(task, parent)
        self.init_ui()
        self.connect_buttons()

    def init_ui(self):
        self.info = text(f"{self.task.comment}", 20, "white")
        self.info.setWordWrap(True)
        self.date = text(f"{self.task.deadline}", 16, "white")
        self.take_button = option_button("Взяти", "rgb(50, 140, 131)")

        self.layout.addWidget(self.info)
        self.layout.addWidget(self.date, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.take_button, alignment=Qt.AlignCenter)

    def connect_buttons(self):
        self.take_button.clicked.connect(lambda: self.take_task())

    def take_task(self):
        from managers.DAO_classes import tasks_DAO
        tasks_DAO.to_next_stage(self.task.id)


class process_task(task_base):
    def __init__(self, task: TaskBase, assigned_stuff: stuff, parent=None):
        super().__init__(task, parent)
        self.assigned_stuff = assigned_stuff
        self.init_ui()
        self.connect_buttons()

    def init_ui(self):
        self.info = text(f"{self.task.comment}", 20, "white")
        self.info.setWordWrap(True)
        self.date = text(f"{self.task.deadline}", 16, "white")
        self.next_stage_button = option_button("Наступний етап", "rgb(91, 26, 105)")

        self.layout.addWidget(self.info)
        self.layout.addWidget(self.date, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.next_stage_button, alignment=Qt.AlignCenter)

    def connect_buttons(self):
        self.next_stage_button.clicked.connect(lambda: self.move_to_next_stage())

    def move_to_next_stage(self):
        """Переводить завдання на наступну стадію."""
        if self.assigned_stuff is None or not hasattr(self.assigned_stuff, 'id'):
            print("Error: Assigned staff is not properly initialized.")
            return

        try:
            tasks_DAO.to_next_stage(self.task.id, self.assigned_stuff.id)
            print(f"Task {self.task.id} successfully moved to the next stage.")
        except Exception as e:
            print(f"Error moving task {self.task.id} to the next stage: {e}")



class done_task(task_base):
    def __init__(self, task: TaskBase, parent=None):
        super().__init__(task, parent)
        self.init_ui()

    def init_ui(self):
        self.info = text(f"{self.task.comment}", 20, "white")
        self.info.setWordWrap(True)
        self.date = text(f"{self.task.deadline}", 16, "white")

        self.layout.addWidget(self.info)
        self.layout.addWidget(self.date, alignment=Qt.AlignLeft)

