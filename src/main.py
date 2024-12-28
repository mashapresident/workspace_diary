import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from interface.windows.login_page import login_page
from managers.resource_path import resource_path
from managers.window_manager import window_manager


def main():
    app = QApplication(sys.argv)
    icon = QIcon(resource_path.get_path("interface/assets/final_icon.png"))
    app.setWindowIcon(icon)
    window_manager.open_page(login_page)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
