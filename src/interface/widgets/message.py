from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QMessageBox

from managers.resource_path import resource_path


class message:
    @staticmethod
    def show_message(type_of_message: str, message: str):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle(type_of_message)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        icon_pixmap = QPixmap(resource_path.get_path("interace/assets/final_icon.png"))
        msg_box.setIconPixmap(icon_pixmap)
        msg_box.exec()
