from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton, QWidget




class button(QPushButton):
     def __init__(self, label: str, parent: QWidget = None):
        super().__init__(label, parent)
        self.setMaximumSize(QSize(380, 50))
        self.setMinimumSize(QSize(380, 50))
        self.setStyleSheet(
            """ 
            QPushButton { 
                background-color: rgb(146, 108, 230);
                font: 24pt "Apple Symbols";
                border: 1px solid rgb(146, 108, 230);
                color: white;
                border-radius: 10px;
            }
            QPushButton:hover { 
                background-color: rgb(124, 100, 200);
            }
            QPushButton:pressed { 
                background-color: rgb(100, 75, 175);
            } 
            """
        )
        
class list_button(QPushButton):
    def __init__(self, label: str, parent: QWidget = None):
        super().__init__(label, parent)
        self.setMaximumSize(QSize(220, 70))
        self.setMinimumSize(QSize(220, 70))
        self.setStyleSheet(
            """ 
            QPushButton { 
                background-color: transparent;
                font: 20pt "Apple Symbols";
                color: white;
            }
            QPushButton[active="true"] {
                background-color: rgb(92, 92, 92); /* Колір для активної кнопки */
                border: 1px solid rgb(150, 150, 150);
            }
            QPushButton:hover { 
                background-color: rgb(69, 69, 69);
            }
            """
        )

class plain_button(QPushButton):
    def __init__(self, label: str, parent: QWidget = None):
        super().__init__(label, parent)
        self.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                color: rgb(146, 108, 230);
                border: none;
                font: 18pt "Apple Symbols";
            }
            QPushButton:hover {
                color: rgb(100, 75, 175);
            }
            """
        )
        
class option_button(QPushButton):
    def __init__(self, label: str, color: str , parent: QWidget = None):
        super().__init__(label, parent)
        self.setFixedHeight(30)
        self.setFixedWidth(70)
        self.setStyleSheet(
            f"""
            QPushButton {{
                background-color: rgb(93, 93, 93);
                color: {color};
                border: none;
                font: 10pt "Apple Symbols";
            }}
            QPushButton:hover {{
                color: rgb(93, 93, 93);
                background-color: {color};
            }}
            """
        )



class icon_button(QPushButton):
    def __init__(self, icon_path: str, parent=None):
        super().__init__(parent)

        # Додавання іконки
        icon = QIcon(icon_path)
        self.setIcon(icon)
        self.setIconSize(QSize(50, 50))  # Розмір іконки всередині кнопки

        # Налаштування круглої форми кнопки
        self.setFixedSize(50, 50)
        self.setStyleSheet(
            """
            QPushButton { 
                background-color: rgb(41, 42, 42); 
                padding: 10px;
                border-radius: 25px; 
            }
            QPushButton:hover {
                background-color: rgb(31,32,32); 
                border-radius: 25px; 
            }
            """
        )
