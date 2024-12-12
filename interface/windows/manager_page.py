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


class PageNames:
    STUFF = "Stuff"
    CUSTOMER = "Customer"
    PROJECT = "Project"
    GROUP = "Group"
    TASK = "Task"


class manager_page(QMainWindow):
    def __init__(self, manager: stuff):
        super().__init__()
        self.manager = manager
        self.opened_project = project_DAO.get_first_project()
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.main_layout = QVBoxLayout(self.centralwidget)
        self.label = text(f"Вітаємо, {self.manager.fullname}", 18, "white")

        # Іконки
        self.add_stuff = icon_button("./interface/assets/add_stuff.png")
        self.add_customer = icon_button("./interface/assets/add_stuff.png")
        self.add_project = icon_button("./interface/assets/add_project.png")
        self.add_group = icon_button("./interface/assets/add_group.png")
        self.make_report = icon_button("./interface/assets/make_report.png")
        self.add_task = icon_button("./interface/assets/add_task.png")

        self.projects_list = project_DAO.get_all_projects()
        self.button_widgets = []

        self.left_layout = QVBoxLayout()
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )  # Вертикальний скрол
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )  # Вимкнено горизонтальний скрол

        self.scroll_widget = QWidget()
        self.scroll_widget.setLayout(self.left_layout)
        self.scroll_area.setWidget(self.scroll_widget)

        self.right_layout = QHBoxLayout()  # Горизонтальний лейаут для контейнерів задач

        # Додавання кнопок проєктів
        for project in self.projects_list:
            button_name = getattr(project, "name", str(project))  # Назва проєкту
            button = list_button(button_name)
            button.clicked.connect(self.handle_button_click)
            self.button_widgets.append(button)
            self.left_layout.addWidget(button)

        self.add_widgets()
        self.connect_buttons()

        # Додавання task_container у правий блок
        self.add_task_containers()

    def add_widgets(self):
        self.resize(1000, 600)
        self.setMinimumSize(QSize(600, 400))
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
        self.main_layout.addLayout(top_layout_buttons)

        # Основний вміст
        self.content_layout = QHBoxLayout()

        self.scroll_area.setFixedWidth(260)  # Ширина блоку зі скролом
        self.scroll_area.setFixedHeight(490)

        # Додавання скрол-зони
        self.content_layout.addWidget(self.scroll_area, alignment=Qt.AlignLeft)
        self.content_layout.addLayout(self.right_layout, 4)  # Правий блок
        self.main_layout.addLayout(self.content_layout)

    @Slot()
    def handle_button_click(self):
        # Отримуємо кнопку, яка викликала сигнал
        clicked_button = self.sender()

        # Скидаємо стан "active" для всіх кнопок
        for button in self.button_widgets:
            button.setProperty("active", False)

        # Встановлюємо "active" для натиснутої кнопки
        clicked_button.setProperty("active", True)

        # Оновлюємо стиль
        for button in self.button_widgets:
            button.style().unpolish(button)
            button.style().polish(button)

        # Отримуємо індекс або проєкт, пов'язаний із натиснутою кнопкою
        button_index = self.button_widgets.index(clicked_button)
        selected_project = self.projects_list[button_index]

        # Зберігаємо вибраний проєкт
        self.opened_project = selected_project

    def add_task_containers(self):
        assigned = task_container(
            "to do", tasks_DAO.get_tasks("given", self.opened_project, "manager"), self
        )
        self.right_layout.addWidget(assigned)

        process = task_container(
            "in the progress",
            tasks_DAO.get_tasks("in the progress", self.opened_project, "manager"),
            self,
        )
        self.right_layout.addWidget(process)

        done = task_container(
            "done", tasks_DAO.get_tasks("done", self.opened_project, "manager"), self
        )
        self.right_layout.addWidget(done)

        checked = task_container(
            "checked",
            tasks_DAO.get_tasks("checked", self.opened_project, "manager"),
            self,
        )
        self.right_layout.addWidget(checked)

    def connect_buttons(self):
        from interface.windows.extra_windows.add_customer import add_customer
        from interface.windows.extra_windows.add_group import add_group
        from interface.windows.extra_windows.add_project import add_project
        from interface.windows.extra_windows.add_stuff import add_stuff
        from interface.windows.extra_windows.add_task import add_task
        from managers.report_manager import report_manager

        self.add_stuff.clicked.connect(
            lambda: window_manager.open_page(add_stuff, PageNames.STUFF)
        )
        self.add_customer.clicked.connect(
            lambda: window_manager.open_page(add_customer, PageNames.CUSTOMER)
        )
        self.add_project.clicked.connect(
            lambda: window_manager.open_page(add_project, PageNames.PROJECT)
        )
        self.add_group.clicked.connect(
            lambda: window_manager.open_page(add_group, PageNames.GROUP)
        )
        self.add_group.clicked.connect(
            lambda: window_manager.open_page(add_task, PageNames.TASK)
        )
        self.make_report.clicked.connect(report_manager.make_report)

    def closeEvent(self, event):
        window_manager.close_all_active_windows()
        event.accept()
