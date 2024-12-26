from PySide6.QtCore import QSize, Qt, Slot
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from database.tables import stuff
from interface.widgets.buttons import icon_button, list_button
from interface.widgets.task_container import task_container
from interface.widgets.text import text
from managers.DAO_classes import project_DAO, tasks_DAO
from managers.window_manager import window_manager


class stuff_page(QMainWindow):
    def __init__(self, stuff: stuff):
        super().__init__()
        self.stuff = stuff
        self.opened_project = None

        # Центральний віджет і основний лейаут
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.main_layout = QVBoxLayout(self.centralwidget)

        # Привітальне повідомлення
        self.label = text(f"Вітаємо, {self.stuff.fullname}", 18, "white")

        # Іконки для верхніх кнопок
        self.reload = icon_button("./interface/assets/reload.png")

        # Список проєктів і кнопки
        self.projects_list = project_DAO.get_all_projects()
        # self.projects_list = project_DAO.get_projects_by_stuff_id(self.stuff.id)
        self.button_widgets = []

        # Ініціалізація лівого лейауту для списку проєктів
        self.left_layout = QVBoxLayout()
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_widget.setLayout(self.left_layout)
        self.scroll_area.setWidget(self.scroll_widget)

        # Додавання кнопок проєктів
        for project in self.projects_list:
            button_name = getattr(project, "name", str(project))  # Назва проєкту
            button = list_button(button_name)
            button.clicked.connect(self.handle_button_click)
            self.button_widgets.append(button)
            self.left_layout.addWidget(button)

        # Контейнери задач
        self.assigned = task_container(
            "to do",
            tasks_DAO.get_tasks("given", self.opened_project, self.stuff.role),
            self,
        )
        self.process = task_container(
            "in the process",
            tasks_DAO.get_tasks("in the process", self.opened_project, self.stuff.role),
            self,
        )
        self.done = task_container(
            "done",
            tasks_DAO.get_tasks("done", self.opened_project, self.stuff.role),
            self,
        )
        self.checked = task_container(
            "checked",
            tasks_DAO.get_tasks("checked", self.opened_project, self.stuff.role),
            self,
        )

        # Додавання всіх віджетів і кнопок
        self.add_widgets()
        self.connect_buttons()

    def add_widgets(self):
        """Метод для додавання віджетів у вікно."""
        self.resize(1200, 800)
        self.setMinimumSize(QSize(1200, 800))
        self.setStyleSheet("background-color: rgb(41, 42, 42)")

        # Привітання
        top_layout_label = QHBoxLayout()
        top_layout_label.addWidget(self.label, alignment=Qt.AlignCenter)
        self.main_layout.addLayout(top_layout_label)

        # Верхній блок кнопок додавання
        top_layout_buttons = QHBoxLayout()
        top_layout_buttons.setSpacing(10)
        top_layout_buttons.addStretch()
        top_layout_buttons.addWidget(self.reload, alignment=Qt.AlignLeft)
        self.main_layout.addLayout(top_layout_buttons)

        # Основний вміст
        self.content_layout = QHBoxLayout()

        # Ліва частина зі списком проєктів
        self.scroll_area.setFixedWidth(260)  # Ширина блоку зі скролом
        self.scroll_area.setFixedHeight(490)
        self.content_layout.addWidget(self.scroll_area, alignment=Qt.AlignLeft)

        # Права частина з контейнерами задач
        self.right_layout = QHBoxLayout()
        self.content_layout.addLayout(self.right_layout, 4)
        self.main_layout.addLayout(self.content_layout)

        self.right_layout.addWidget(self.assigned)
        self.right_layout.addWidget(self.process)
        self.right_layout.addWidget(self.done)
        self.right_layout.addWidget(self.checked)

    @Slot()
    def handle_button_click(self):
        """Обробка натискання на кнопку проєкту."""
        clicked_button = self.sender()

        # Deselect all buttons
        for button in self.button_widgets:
            button.setProperty("active", False)

        # Select the clicked button
        clicked_button.setProperty("active", True)

        # Update the style of the clicked button
        for button in self.button_widgets:
            button.style().unpolish(button)
            button.style().polish(button)

        # Get the index of the clicked button
        button_index = self.button_widgets.index(clicked_button)

        # Get the selected project
        selected_project = self.projects_list[button_index]
        self.opened_project = selected_project

        # Update the task containers with tasks from the new project
        self.update_task_containers()

    def update_task_containers(self):
        """Оновлює контейнери задач для вибраного проєкту."""
        self.assigned.update_tasks(
            tasks_DAO.get_tasks("given", self.opened_project, "manager")
        )
        self.process.update_tasks(
            tasks_DAO.get_tasks("in the process", self.opened_project, "manager")
        )
        self.done.update_tasks(
            tasks_DAO.get_tasks("done", self.opened_project, "manager")
        )
        self.checked.update_tasks(
            tasks_DAO.get_tasks("checked", self.opened_project, "manager")
        )

    def connect_buttons(self):

        self.reload.clicked.connect(self.update_task_containers)

    def closeEvent(self, event):
        window_manager.close_all_active_windows()
        event.accept()
