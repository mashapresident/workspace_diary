from PySide6.QtCore import QCoreApplication, QSize, Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QWidget,
)


class stuff_page(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 400, 300)
