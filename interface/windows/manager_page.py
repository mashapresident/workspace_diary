from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from database.tables import stuff
from interface.widgets.buttons import icon_button
from interface.widgets.text import text
from managers.DAO_classes import project_DAO
from managers.window_manager import window_manager


class manager_page(QMainWindow):
    def __init__(self, manager: stuff):
        super().__init__()
        self.manager = manager
        self.resize(1000, 600)
        self.setMinimumSize(QSize(600, 400))
        self.setStyleSheet("background-color: rgb(41, 42, 42)")
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

        # Основний вертикальний макет
        self.main_layout = QVBoxLayout(self.centralwidget)

        # Привітальне повідомлення
        self.label = text(f"Вітаємо, {self.manager.fullname}", 18, "white")

        # Кнопки додавання проєктів та співробітників
        self.add_stuff = icon_button("./interface/assets/add_stuff.png")
        self.add_customer = icon_button("./interface/assets/add_stuff.png")
        self.add_project = icon_button("./interface/assets/add_project.png")
        self.add_group = icon_button("./interface/assets/add_group.png")
        self.make_report = icon_button("./interface/assets/make_report.png")

        # Додати віджети на сторінку
        self.add_widgets()
        self.connect_buttons()

    def add_widgets(self):
        # Додавання привітального повідомлення
        top_layout_label = QHBoxLayout()
        top_layout_label.addWidget(self.label, alignment=Qt.AlignCenter)
        self.main_layout.addLayout(top_layout_label)

        # Верхній шар із кнопками додавання, вирівняний по правому краю
        top_layout_buttons = QHBoxLayout()
        top_layout_buttons.setSpacing(10)  # Простір між кнопками
        top_layout_buttons.addStretch()  # Додаємо розтягнення зліва для вирівнювання кнопок вправо
        top_layout_buttons.addWidget(self.add_stuff)
        top_layout_buttons.addWidget(self.add_customer)
        top_layout_buttons.addWidget(self.add_project)
        top_layout_buttons.addWidget(self.add_group)
        top_layout_buttons.addWidget(self.make_report)
        self.main_layout.addLayout(top_layout_buttons)

        # Основний шар під верхнім
        self.content_layout = QHBoxLayout()

        # Лівий вертикальний шар із кнопками проєктів
        self.left_layout = QVBoxLayout()
        self.projects_list = project_DAO.get_all_projects()
        self.button_widgets = []

        # Додавання кнопок проєктів
        for project in self.projects_list:
            # Отримати назву проєкту (припускаємо, що це атрибут або ключ словника)
            button_name = getattr(
                project, "name", str(project)
            )  # Якщо атрибута `name` немає, перетворюємо на рядок
            button = QPushButton(button_name)
            button.clicked.connect(lambda _, btn=button: self.switch_to_text(btn))
            self.button_widgets.append(button)
            self.left_layout.addWidget(button)

        # Правий шар із 5 вертикальними секціями
        self.right_layout = QVBoxLayout()
        for i in range(5):
            layer = QVBoxLayout()
            widget = QLabel(f"Widget {i + 1}")
            widget.setAlignment(Qt.AlignCenter)
            layer.addWidget(widget)
            self.right_layout.addLayout(layer)

        # Додавання лівого та правого шарів у основний шар контенту
        self.content_layout.addLayout(self.left_layout, 1)
        self.content_layout.addLayout(self.right_layout, 4)
        self.main_layout.addLayout(self.content_layout)

    def switch_to_text(self, button):
        # Заміна натиснутої кнопки на текст
        label = QLabel(button.text())
        label.setAlignment(Qt.AlignCenter)
        index = self.left_layout.indexOf(button)
        if index != -1:
            self.left_layout.replaceWidget(button, label)
            button.deleteLater()

    def connect_buttons(self):
        from interface.windows.extra_windows.add_customer import add_customer
        from interface.windows.extra_windows.add_group import add_group
        from interface.windows.extra_windows.add_project import add_project
        from interface.windows.extra_windows.add_stuff import add_stuff
        from managers.report_manager import report_manager

        # Підключення кнопок до методів відкриття нових сторінок
        self.add_stuff.clicked.connect(lambda: window_manager.go_to_page(add_stuff))
        self.add_customer.clicked.connect(
            lambda: window_manager.go_to_page(add_customer)
        )
        self.add_project.clicked.connect(lambda: window_manager.go_to_page(add_project))
        self.add_group.clicked.connect(lambda: window_manager.go_to_page(add_group))
        self.make_report.clicked.connect(report_manager.make_report)
