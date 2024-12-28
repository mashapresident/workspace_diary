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
from managers.DAO_classes import stuff_DAO
from managers.extra_windows_manager import extra_windows_manager


class add_group(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1200, 800)
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

        for staff_member in stuff_DAO.get_all_stuff_without_manager():
            item = QListWidgetItem(staff_member.fullname)
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
        self.add_group.clicked.connect(
            lambda: extra_windows_manager.add_group(
                self.name_of_group.text(),
                [item.text() for item in self.group_list.selectedItems()],
            )
        )
        self.back_button.clicked.connect(self.close)
