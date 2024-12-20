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
from interface.windows.extra_windows.page_names import page_names
from managers.DAO_classes import project_DAO, tasks_DAO
from managers.window_manager import window_manager


class manager_page(QMainWindow):
    def __init__(self, manager: stuff):
        super().__init__()
        self.manager = manager
        self.opened_project = None

        # Центральний віджет і основний лейаут
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.main_layout = QVBoxLayout(self.centralwidget)

        # Привітальне повідомлення
        self.label = text(f"Вітаємо, {self.manager.fullname}", 18, "white")

        # Іконки для верхніх кнопок
        self.add_stuff = icon_button("./interface/assets/add_stuff.png")
        self.add_customer = icon_button("./interface/assets/add_stuff.png")
        self.add_project = icon_button("./interface/assets/add_project.png")
        self.add_group = icon_button("./interface/assets/add_group.png")
        self.make_report = icon_button("./interface/assets/make_report.png")
        self.add_task = icon_button("./interface/assets/add_task.png")

        # Список проєктів і кнопки
        self.projects_list = project_DAO.get_all_projects()
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
            "to do", tasks_DAO.get_tasks("given", self.opened_project, "manager"), self
        )
        self.process = task_container(
            "in the process",
            tasks_DAO.get_tasks("in the process", self.opened_project, "manager"),
            self,
        )
        self.done = task_container(
            "done", tasks_DAO.get_tasks("done", self.opened_project, "manager"), self
        )
        self.checked = task_container(
            "checked",
            tasks_DAO.get_tasks("checked", self.opened_project, "manager"),
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
        top_layout_buttons.addWidget(self.add_stuff)
        top_layout_buttons.addWidget(self.add_customer)
        top_layout_buttons.addWidget(self.add_project)
        top_layout_buttons.addWidget(self.add_group)
        top_layout_buttons.addWidget(self.make_report)
        top_layout_buttons.addWidget(self.add_task)
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
        """Метод для з'єднання кнопок з діями."""
        from interface.windows.extra_windows.add_customer import add_customer
        from interface.windows.extra_windows.add_group import add_group
        from interface.windows.extra_windows.add_project import add_project
        from interface.windows.extra_windows.add_report import add_report
        from interface.windows.extra_windows.add_stuff import add_stuff
        from interface.windows.extra_windows.add_task import add_task

        self.add_stuff.clicked.connect(
            lambda: window_manager.open_page(add_stuff, page_names.STUFF)
        )
        self.add_customer.clicked.connect(
            lambda: window_manager.open_page(add_customer, page_names.CUSTOMER)
        )
        self.add_project.clicked.connect(
            lambda: window_manager.open_page(add_project, page_names.PROJECT)
        )
        self.add_group.clicked.connect(
            lambda: window_manager.open_page(add_group, page_names.GROUP)
        )
        self.add_task.clicked.connect(
            lambda: window_manager.open_page(add_task, page_names.TASK)
        )
        self.make_report.clicked.connect(
            lambda: window_manager.open_page(add_report, page_names.REPORT)
        )

    def closeEvent(self, event):
        """Закриття всіх активних вікон при закритті."""
        window_manager.close_all_active_windows()
        event.accept()
