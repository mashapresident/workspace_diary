from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from interface.widgets.buttons import button, icon_button
from interface.widgets.qlines import parent_line
from managers.DAO_classes import groups_DAO, stuff_DAO, stuff_group_DAO


class add_group(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1000, 600)
        self.setMinimumSize(QSize(1000, 600))
        self.setStyleSheet("background-color: rgb(41, 42, 42)")
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

        self.verticalLayoutWidget = QVBoxLayout(self.centralwidget)
        self.verticalLayoutWidget.setSpacing(20)
        self.verticalLayoutWidget.setContentsMargins(20, 60, 20, 60)

        self.back_button = icon_button("./interface/assets/back_button.png")
        self.name_of_group = parent_line("Назва групи")
        self.group_list = QListWidget()
        self.group_list.setFixedWidth(800)
        self.group_list.setSelectionMode(QListWidget.MultiSelection)
        self.group_list.setStyleSheet(
            "background-color: rgb(94, 84, 117);\n"
            'font: 15pt "Apple Symbols";\n'
            "color: black;\n "
            "border-radius: 5px\n"
        )

        # Добавление сотрудников в список с чекбоксами
        for staff_member in stuff_DAO.get_all_stuff_without_manager():
            item = QListWidgetItem(
                staff_member.fullname
            )  # Предполагается, что объекты staff имеют атрибут name
            item.setCheckState(Qt.Unchecked)
            self.group_list.addItem(item)

        self.add_group = button("Додати")
        self.add_widgets()
        self.connect_buttons()

    def add_widgets(self):
        self.verticalLayoutWidget.addWidget(
            self.back_button, alignment=Qt.AlignTop | Qt.AlignLeft
        )
        self.verticalLayoutWidget.addWidget(
            self.name_of_group, alignment=Qt.AlignCenter
        )
        self.verticalLayoutWidget.addWidget(self.group_list, alignment=Qt.AlignCenter)
        self.verticalLayoutWidget.addWidget(self.add_group, alignment=Qt.AlignCenter)

    def connect_buttons(self):
        self.add_group.clicked.connect(self.add_group_to_database)
        self.back_button.clicked.connect(self.close)

    def add_group_to_database(self):
        from interface.widgets.message import message

        # Проверяем, что название группы и список сотрудников заполнены
        if not self.name_of_group.text():
            message.show_message("Помилка", "Назва групи не може бути порожньою")
            return
        elif self.group_list.count() == 0:
            message.show_message("Помилка", "Група не може бути порожньою")
            return

        # Добавляем новую группу и получаем её ID
        group_name = self.name_of_group.text()
        groups_DAO.add_group(group_name)

        group_id = groups_DAO.get_group_id_by_name(group_name)

        # Добавляем сотрудников в группу
        for index in range(self.group_list.count()):
            item = self.group_list.item(index)
            if item.checkState() == Qt.Checked:
                # Получаем ID сотрудника по его имени
                staff_id = stuff_DAO.get_staff_id_by_fullname(item.text())
                # Добавляем сотрудника в группу
                stuff_group_DAO.add_stuff_to_group(staff_id, group_id)

        message.show_message("Успішно", f"Група '{group_name}' додана")
