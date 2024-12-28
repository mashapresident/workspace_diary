from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from database.tables import customer


class customer_view(QPushButton):
    def __init__(self, cust:customer, parent=None):
        super().__init__(parent)
        self.customer = cust
        
        self.setFixedHeight(80)
        self.setStyleSheet(
            """
            QPushButton {
                background-color: rgb(150, 150, 150);
                color: rgb(0, 0, 0);
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: rgb(100, 100, 100); 
                color: rgb(0, 0, 0); 
                border-radius: 20px;
            }
            """
        )
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 5, 10, 5)
        
        
        text_layout = QVBoxLayout()
        name_label = QLabel(self.contact.name)
        name_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        
        text_layout.addWidget(name_label)

        
        main_layout.addLayout(text_layout)
        
        # Optional: Connect button to slot or function
        self.clicked.connect(self.w_manager.go_to_page())