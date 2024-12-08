from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel

class text(QLabel):
    def __init__(self, text: str, size: int, color: str):
        super().__init__(text)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(
            f'font: {size}px "Apple Symbols";\n'
            "border: none;\n"
            f"color: {color};"
        )
