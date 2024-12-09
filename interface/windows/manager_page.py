from PySide6.QtCore import QSize, Qt, Slot
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QScrollArea
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
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.main_layout = QVBoxLayout(self.centralwidget)
        self.label = text(f"Вітаємо, {self.manager.fullname}", 18, "white")

        self.add_stuff = icon_button("./interface/assets/add_stuff.png")
        self.add_customer = icon_button("./interface/assets/add_stuff.png")
        self.add_project = icon_button("./interface/assets/add_project.png")
        self.add_group = icon_button("./interface/assets/add_group.png")

        self.projects_list = project_DAO.get_all_projects()
        self.button_widgets = []

        # Лівий блок як окремий скрол
        self.left_layout = QVBoxLayout()
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_widget.setLayout(self.left_layout)
        self.scroll_area.setWidget(self.scroll_widget)

        self.right_layout = QVBoxLayout()  # Додано правий шар

        # Додавання кнопок проєктів у left_layout
        for project in self.projects_list:
            button_name = getattr(project, "name", str(project))  # Назва проєкту
            button = QPushButton(button_name)
            button.setMaximumSize(QSize(300, 80))
            button.setMinimumSize(QSize(300, 80))
            button.setStyleSheet(
                """ 
                QPushButton { 
                    font: 40pt "Apple Symbols";
                    color: white;
                } 
                """
            )
            button.clicked.connect(self.handle_button_click)
            self.button_widgets.append(button)
            self.left_layout.addWidget(button)

        self.add_widgets()
        self.connect_buttons()

    def add_widgets(self):
        self.resize(1000, 600)
        self.setMinimumSize(QSize(600, 400))
        self.setStyleSheet("background-color: rgb(41, 42, 42)")
        
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
        self.main_layout.addLayout(top_layout_buttons)

        # Основний шар під верхнім
        self.content_layout = QHBoxLayout()

        # Налаштування розмірів для скролу (80% висоти, 25% ширини)
        self.scroll_area.setFixedWidth(int(self.width() * 0.25))  # 25% ширини
        self.scroll_area.setFixedHeight(int(self.height() * 0.8))  # 80% висоти

        # Додавання скрол-зони у лівий блок
        self.content_layout.addWidget(self.scroll_area, alignment=Qt.AlignLeft)
        self.content_layout.addLayout(self.right_layout, 4)  # Правий блок
        self.main_layout.addLayout(self.content_layout)

    @Slot()
    def handle_button_click(self):
        # Отримуємо кнопку, яка викликала сигнал
        clicked_button = self.sender()

        # Скидаємо всі кнопки до початкового кольору
        for button in self.button_widgets:
            button.setStyleSheet("background-color:  transparent;")

        # Міняємо колір активної кнопки
        clicked_button.setStyleSheet("background-color: rgb(92, 92, 92);")

    def connect_buttons(self):
        from interface.windows.extra_windows.add_customer import add_customer
        from interface.windows.extra_windows.add_group import add_group
        from interface.windows.extra_windows.add_project import add_project
        from interface.windows.extra_windows.add_stuff import add_stuff

        self.add_stuff.clicked.connect(lambda: window_manager.open_page(add_stuff))
        self.add_customer.clicked.connect(
            lambda: window_manager.open_page(add_customer)
        )
        self.add_project.clicked.connect(lambda: window_manager.open_page(add_project))
        self.add_group.clicked.connect(lambda: window_manager.open_page(add_group))
