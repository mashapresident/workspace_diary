from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import Slot

class ColorChangingButtons(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Кнопки, що змінюють колір")
        
        # Початковий і активний кольори
        self.default_color = "background-color: lightgray;"
        self.active_color = "background-color: lightblue;"
        
        # Layout для кнопок
        self.layout = QVBoxLayout()
        
        # Список кнопок
        self.buttons = []
        for i in range(5):  # Наприклад, 5 кнопок
            button = QPushButton(f"Кнопка {i+1}")
            button.setStyleSheet(self.default_color)
            button.clicked.connect(self.handle_button_click)
            self.buttons.append(button)
            self.layout.addWidget(button)
        
        self.setLayout(self.layout)
    
    @Slot()
    def handle_button_click(self):
        # Отримуємо кнопку, яка викликала сигнал
        clicked_button = self.sender()
        
        # Скидаємо всі кнопки до початкового кольору
        for button in self.buttons:
            button.setStyleSheet(self.default_color)
        
        # Міняємо колір активної кнопки
        clicked_button.setStyleSheet(self.active_color)

if __name__ == "__main__":
    app = QApplication([])
    window = ColorChangingButtons()
    window.show()
    app.exec()
