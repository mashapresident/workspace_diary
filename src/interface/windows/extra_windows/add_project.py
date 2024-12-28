from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from interface.widgets.buttons import button, icon_button
from interface.widgets.qlines import (
    cost_line,
    customer_choice,
    groups_choice,
    parent_line,
)
from managers.DAO_classes import customer_DAO, groups_DAO
from managers.extra_windows_manager import extra_windows_manager
from managers.resource_path import resource_path


class add_project(QMainWindow):
    def __init__(self):
        super().__init__()
        self.back_button = icon_button(
            resource_path.get_path("interface/assets/back_button.png")
        )
        self.name_line = parent_line("Назва")
        self.group = groups_choice(groups_DAO.get_groups())
        self.customer = customer_choice(customer_DAO.get_all_customers())
        self.cost_line = cost_line("Вартість")
        self.paid_line = cost_line("Оплачено")
        self.add_button = button("Додати")
        self.add_widgets()
        self.connect_buttons()

    def add_widgets(self):
        self.resize(1200, 800)
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
        self.add_button.clicked.connect(
            lambda: extra_windows_manager.add_project(
                name=self.name_line.text(),
                group_name=self.group.currentText(),
                customer_name=self.customer.currentText(),
                cost=self.cost_line.text(),
                paid=self.paid_line.text(),
            )
        )
        self.back_button.clicked.connect(self.close)
