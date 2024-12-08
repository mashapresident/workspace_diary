from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QCheckBox, QLabel, QPushButton
)
import sys

class CheckBoxExample(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CheckBox Example")
        self.setGeometry(100, 100, 300, 200)

        # Создание центрального виджета и вертикального слоя
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)

        # Создание метки
        self.label = QLabel("Выберите опции:", self)
        layout.addWidget(self.label)

        # Добавление чекбоксов
        self.check1 = QCheckBox("Option 1", self)
        self.check2 = QCheckBox("Option 2", self)
        self.check3 = QCheckBox("Option 3", self)

        layout.addWidget(self.check1)
        layout.addWidget(self.check2)
        layout.addWidget(self.check3)

        # Кнопка для отображения выбранных опций
        self.button = QPushButton("Show Selected Options", self)
        self.button.clicked.connect(self.show_selected_options)
        layout.addWidget(self.button)

        # Установка центрального виджета
        self.setCentralWidget(central_widget)

    def show_selected_options(self):
        # Получение состояния чекбоксов
        selected_options = []
        if self.check1.isChecked():
            selected_options.append("Option 1")
        if self.check2.isChecked():
            selected_options.append("Option 2")
        if self.check3.isChecked():
            selected_options.append("Option 3")

        # Вывод выбранных опций
        self.label.setText(f"Выбрано: {', '.join(selected_options)}")

# Запуск приложения
app = QApplication(sys.argv)
window = CheckBoxExample()
window.show()
sys.exit(app.exec())
