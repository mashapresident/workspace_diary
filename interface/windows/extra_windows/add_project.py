from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from interface.widgets.buttons import button, icon_button
from interface.widgets.message import message
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
        self.add_button.clicked.connect(self.add_project_to_database)
        self.back_button.clicked.connect(self.close)

    def add_project_to_database(self):
        if not( self.name_line.text() or self.name_line.text() or self.paid_line.text()):
            message.show_message("Помилка", "Не всі поня заповнені")
            return
        
        name = self.name_line.text()
        group_id = groups_DAO.get_group_id_by_name(self.group.currentText()) 
        customer_id = customer_DAO.get_customer_id_by_fullname(self.customer.currentText())
        cost =  self.name_line.text()
        paid = self.paid_line.text()

       
        
        project_DAO.add_project(name, group_id, customer_id, int(cost), int(paid))
        message.show_message("Успішно", "Проєкт створено")
