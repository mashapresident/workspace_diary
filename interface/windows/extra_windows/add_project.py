from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from interface.widgets.buttons import button, icon_button
from interface.widgets.qlines import (
    cost_line,
    customer_choice,
    groups_choice,
    parent_line,
)
from managers.DAO_classes import customer_DAO, groups_DAO, project_DAO


class add_project(QMainWindow):
    def __init__(self):
        super().__init__()
        self.back_button = icon_button("./interface/assets/back_button.png")
        self.name_line = parent_line("Назва")
        self.group = groups_choice(groups_DAO.get_groups())
        print(groups_DAO.get_groups())
        self.customer = customer_choice(customer_DAO.get_all_customers())
        self.cost_line = cost_line("Вартість")
        self.paid_line = cost_line("Оплачено")
        self.add_button = button("Додати")
        self.add_widgets()
        self.connect_buttons()

    def add_widgets(self):
        self.setWindowTitle("Adding Project")
        self.resize(1000, 600)
        self.setMinimumSize(QSize(1000, 600))
        self.setStyleSheet("background-color: rgb(41, 42, 42)")
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

        self.verticalLayoutWidget = QVBoxLayout(self.centralwidget)
        self.verticalLayoutWidget.setSpacing(20)
        self.verticalLayoutWidget.setContentsMargins(20, 60, 20, 60)
        self.verticalLayoutWidget.addWidget(
            self.back_button, alignment=Qt.AlignTop | Qt.AlignLeft
        )
        self.verticalLayoutWidget.addWidget(self.name_line, alignment=Qt.AlignCenter)
        self.verticalLayoutWidget.addWidget(self.group, alignment=Qt.AlignCenter)
        self.verticalLayoutWidget.addWidget(self.customer, alignment=Qt.AlignCenter)
        self.verticalLayoutWidget.addWidget(self.cost_line, alignment=Qt.AlignCenter)
        self.verticalLayoutWidget.addWidget(self.paid_line, alignment=Qt.AlignCenter)
        self.verticalLayoutWidget.addWidget(self.add_button, alignment=Qt.AlignCenter)

    def connect_buttons(self):
        self.add_button.clicked.connect(self.add_project_to_database)
        self.back_button.clicked.connect(self.close)

    def add_project_to_database(self):
        name = self.name_line.text()
        group_id = self.group.currentIndex() + 1  # или получаем id группы из объекта
        customer_id = (
            self.customer.selected_items[0] if self.customer.selected_items else None
        )  # Получаем id клиента
        cost = self.cost_line.text()
        paid = self.paid_line.text()

        # Добавление проекта в базу данных
        if customer_id is not None:
            project_DAO.add_project(name, group_id, customer_id, int(cost), int(paid))
        else:
            print("замовника не обрано")
