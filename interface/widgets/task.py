from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from database.tables import task
from interface.widgets.text import text
from interface.widgets.buttons import plain_button


class task(QWidget):
    def __init__(self, task: task, parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            """
        background-color: rgb(213, 186, 217);
        border-radius: 5px;
        padding: 5px 10px;
        """
        )
        self.label = text(f"Завдання {task.id}", 18, "black")
        self.info = text(f"{task.comment}", 16, " rgb(36, 7, 41)")
        self.date = text(f"{task.deadline}", 16, " rgb(36, 7, 41)")
        
        self.take_button = plain_button("")
