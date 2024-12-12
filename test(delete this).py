from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class check_box(QComboBox):
    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        self.setFixedSize(800, 40)
        self.setPlaceholderText(text)
        self.setStyleSheet(
            "background-color: rgb(188, 191, 191);\n"
            'font: 20pt "Apple Symbols";\n'
            "color: rgb(146, 108, 230);\n "
            "border-radius: 3px"
        )
        self.dialog = None

        # Add some items to the combo box for demonstration
        self.addItem("Option 1")
        self.addItem("Option 2")
        self.addItem("Option 3")

        # Button to show the dialog
        self.show_dialog_button = QPushButton(text)
        self.show_dialog_button.clicked.connect(self.show_dialog)

    def show_dialog(self):
        if not self.dialog:
            self.dialog = QDialog()
            self.dialog.setWindowTitle("Dialog Example")
            self.dialog.setFixedSize(300, 150)
            label = QLabel("This is a dialog!", self.dialog)
            label.move(50, 50)
        self.dialog.exec()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom ComboBox Example")

        layout = QVBoxLayout(self)

        # Instantiate the custom check_box (QComboBox subclass)
        combo_box = check_box("Select Option", self)
        layout.addWidget(combo_box)

        # Add the button to layout
        layout.addWidget(combo_box.show_dialog_button)

        self.setLayout(layout)
        self.show()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    app.exec_()
